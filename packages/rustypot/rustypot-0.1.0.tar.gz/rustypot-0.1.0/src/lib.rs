use std::{
    sync::{Arc, Mutex, RwLock},
    thread,
    time::{Duration, Instant},
    vec,
};

use pyo3::{exceptions::PyIOError, prelude::*};

use ::rustypot::{self as r, device::feetech_sts3215};

#[pyclass]
struct IO {
    io: r::DynamixelSerialIO,
    serial_port: Mutex<Box<dyn serialport::SerialPort>>,
}

#[pymethods]
impl IO {
    fn read_present_position(&self, ids: Vec<u8>) -> PyResult<Vec<f64>> {
        let mut serial_port = self.serial_port.lock().unwrap();
        feetech_sts3215::sync_read_present_position(&self.io, serial_port.as_mut(), &ids)
            .map(|pos| {
                pos.into_iter()
                    .map(feetech_sts3215::conv::dxl_pos_to_radians)
                    .collect()
            })
            .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }

    // not good ?
    fn read_present_velocity(&self, ids: Vec<u8>) -> PyResult<Vec<f64>> {
        let mut serial_port = self.serial_port.lock().unwrap();

        feetech_sts3215::sync_read_present_speed(&self.io, serial_port.as_mut(), &ids)
            .map(|speeds| {
                speeds
                    .into_iter()
                    .map(|x| feetech_sts3215::conv::dxl_to_speed(x as u16))
                    .collect()
            })
            .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }

    fn write_goal_position(&self, ids: Vec<u8>, goal_position: Vec<f64>) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        let goal_position: Vec<i16> = goal_position
            .into_iter()
            .map(feetech_sts3215::conv::radians_to_dxl_pos)
            .collect();

        feetech_sts3215::sync_write_goal_position(
            &self.io,
            serial_port.as_mut(),
            &ids,
            &goal_position,
        )
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }

    fn set_mode(&self, ids: Vec<u8>, mode: u8) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        feetech_sts3215::sync_write_mode(
            &self.io,
            serial_port.as_mut(),
            &ids,
            &vec![mode; ids.len()],
        )
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }

    fn set_kps(&self, ids: Vec<u8>, kps: Vec<f64>) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        // use sync_write_p_coefficient

        // feetech_sts3215::sync_write_p_coefficient(&self.io, serial_port.as_mut(), &ids, &kps)
        //     .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
        //expected `&[u8]`, found `&Vec<f64>
        // print the values of d_coefficient
        let d_coefficient = feetech_sts3215::sync_read_d_coefficient(&self.io, serial_port.as_mut(), &ids)
            .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;

        println!("d_coefficient: {:?}", d_coefficient);

        let kps: Vec<u8> = kps.iter().map(|x| *x as u8).collect();

        feetech_sts3215::sync_write_p_coefficient(&self.io, serial_port.as_mut(), &ids, &kps)
            .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))

    }

    fn set_kds(&self, ids: Vec<u8>, kds: Vec<f64>) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        let kds: Vec<u8> = kds.iter().map(|x| *x as u8).collect();

        feetech_sts3215::sync_write_d_coefficient(&self.io, serial_port.as_mut(), &ids, &kds)
            .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }

    fn enable_torque(&self, ids: Vec<u8>) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        feetech_sts3215::sync_write_torque_enable(
            &self.io,
            serial_port.as_mut(),
            &ids,
            &vec![true as u8; ids.len()],
        )
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }
    fn disable_torque(&self, ids: Vec<u8>) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        feetech_sts3215::sync_write_torque_enable(
            &self.io,
            serial_port.as_mut(),
            &ids,
            &vec![false as u8; ids.len()],
        )
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }

    fn set_goal_time(&self, ids: Vec<u8>, goal_time: Vec<u16>) -> PyResult<()> {
        let mut serial_port = self.serial_port.lock().unwrap();

        feetech_sts3215::sync_write_goal_time(&self.io, serial_port.as_mut(), &ids, &goal_time)
            .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    }
}

struct SerialportError(serialport::Error);
impl From<SerialportError> for PyErr {
    fn from(error: SerialportError) -> Self {
        PyIOError::new_err(error.0.to_string())
    }
}

#[pyclass]
struct FeetechController {
    kps: Arc<RwLock<Vec<f64>>>,
    goal_pos: Arc<RwLock<Vec<f64>>>,
    current_speed: Arc<RwLock<Vec<f64>>>,
    present_pos: Arc<RwLock<Vec<f64>>>,
    io: Arc<IO>,
    ids: Arc<Vec<u8>>,
}

#[pymethods]
impl FeetechController {
    #[new]
    fn new(
        serialport: String,
        baudrate: u32,
        update_freq: f32,
        ids: Vec<u8>,
        kps: Vec<f64>,
        init_pos: Vec<f64>,
    ) -> PyResult<Self> {
        let io = Arc::new(feetech(&serialport, baudrate).unwrap());
        let present_pos = io.read_present_position(ids.clone()).unwrap();

        // Setup IO and motors
        io.set_mode(ids.clone(), 2)?;

        let kps = Arc::new(RwLock::new(kps));
        let goal_pos = Arc::new(RwLock::new(init_pos.clone()));
        let current_speed = Arc::new(RwLock::new(vec![0.0; ids.len()]));
        let present_pos = Arc::new(RwLock::new(present_pos));
        let ids = Arc::new(ids);

        let c = FeetechController {
            kps: kps.clone(),
            goal_pos: goal_pos.clone(),
            current_speed: current_speed.clone(),
            present_pos: present_pos.clone(),
            io: io.clone(),
            ids: ids.clone(),
        };

        let period = Duration::from_secs_f32(1.0 / update_freq);

        let goal_pos = goal_pos.clone();
        let kps = kps.clone();
        let present_pos_arc = present_pos.clone();
        let ids = ids.clone();
        let io = io.clone();

        thread::spawn(move || {
            const SPEED_DECIMATION: u32 = 2;
            let mut speed_decimation_index = 0;
            let mut last_t = Instant::now();
            let mut last_pos = vec![0.0; ids.as_ref().len()];

            loop {
                let tic = Instant::now();
                let present_pos: Vec<f64> = io
                    .read_present_position(ids.as_ref().to_vec())
                    .unwrap()
                    .iter()
                    .map(|x| x.to_degrees())
                    .collect();

                // {
                //     let mut stored_pos = present_pos_arc.write().unwrap();
                //     stored_pos.clone_from_slice(&present_pos);
                // }

                // let goal_pos = {
                //     let goal_pos = goal_pos.read().unwrap();
                //     goal_pos.clone()
                // };

                // let kps = {
                //     let kps = kps.read().unwrap();
                //     kps.clone()
                // };

                // let mut pwms = vec![];
                // for i in 0..ids.as_ref().len() {
                //     let error = goal_pos[i] - present_pos[i];
                //     let pwm = kps[i] * error;
                //     let pwm = pwm.clamp(-1000.0, 1000.0);
                //     let pwm = pwm as i16;
                //     pwms.push(pwm);
                // }

                // let pwm_magnitudes: Vec<u16> = pwms.iter().map(|x| x.abs() as u16).collect();
                // let direction_bits: Vec<u16> =
                //     pwms.iter().map(|x| if x >= &0 { 1 } else { 0 }).collect();

                // let mut goal_times = vec![];
                // for i in 0..ids.as_ref().len() {
                //     let goal_time = (direction_bits[i] << 10) | pwm_magnitudes[i];
                //     goal_times.push(goal_time);
                // }

                // io.set_goal_time(ids.as_ref().to_vec(), goal_times).unwrap();

                // if speed_decimation_index % SPEED_DECIMATION == 0 {
                //     let mut speeds = vec![];
                //     let dt = last_t.elapsed().as_secs_f64();
                //     for i in 0..ids.as_ref().len() {
                //         let speed = (present_pos[i] - last_pos[i]) / dt;
                //         speeds.push(speed);
                //     }

                //     {
                //         let mut current_speed = current_speed.write().unwrap();
                //         current_speed.clone_from_slice(&speeds);
                //     }

                //     last_pos = present_pos.clone();
                //     last_t = Instant::now();
                // }

                // speed_decimation_index += 1;

                let toc = Instant::now();
                let elapsed = toc.saturating_duration_since(tic);
                println!("Elapsed: {:?}", elapsed);
                // let elapsed = toc - tic;
                // let sleep_time = period - elapsed;

                // sleep time is period - min(elapsed, period)
                let sleep_time = period
                    .checked_sub(elapsed)
                    .unwrap_or_else(|| Duration::from_secs(0));

                if sleep_time.as_secs_f64() <= 0.0 {
                    eprintln!("Warning: loop took longer than period");
                } else {
                    thread::sleep(sleep_time);
                }
            }
        });
        Ok(c)
    }
    fn set_new_target(&mut self, goal_pos: Vec<f64>) -> PyResult<()> {
        self.goal_pos.write().unwrap().clone_from_slice(&goal_pos);

        Ok(())
    }
    fn set_new_kps(&mut self, kps: Vec<f64>) -> PyResult<()> {
        self.kps.write().unwrap().clone_from_slice(&kps);

        Ok(())
    }
    fn get_current_speed(&self) -> PyResult<Vec<f64>> {
        Ok(self.current_speed.read().unwrap().clone())
    }

    fn get_present_position(&self) -> PyResult<Vec<f64>> {
        Ok(self.present_pos.read().unwrap().clone())
    }

    fn disable_torque(&self) -> PyResult<()> {
        let ids = self.ids.as_ref().to_vec();
        self.io.set_mode(ids.clone(), 0)?;
        self.io.disable_torque(ids)?;
        Ok(())
    }

    fn freeze(&self) -> PyResult<()> {
        let ids = self.ids.as_ref().to_vec();
        let present_position = self.io.read_present_position(ids.clone())?;
        self.io.write_goal_position(ids.clone(), present_position)?;
        self.io.set_mode(ids.clone(), 0)?;
        self.io.enable_torque(ids.clone())?;
        Ok(())
    }
}

#[pyfunction]
fn feetech(serialportname: &str, baudrate: u32) -> PyResult<IO> {
    let serial_port = serialport::new(serialportname, baudrate)
        .timeout(Duration::from_millis(1000))
        .open()
        .map_err(SerialportError)?;
    let serial_port = Mutex::new(serial_port);

    let io = r::DynamixelSerialIO::feetech();

    Ok(IO { io, serial_port })
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustypot(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(feetech, m)?)?;

    m.add_class::<FeetechController>()?;

    Ok(())
}
