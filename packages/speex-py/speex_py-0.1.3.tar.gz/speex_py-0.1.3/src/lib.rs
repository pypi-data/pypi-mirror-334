use pyo3::prelude::*;
use pyo3::types::PyBytes;
use std::env;
use std::ffi::c_int;
use std::os::raw::c_void;
use std::slice;

// Include the generated bindings
#[allow(non_upper_case_globals)]
#[allow(non_camel_case_types)]
#[allow(non_snake_case)]
mod bindings {
    include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
}

use bindings::*;

#[pyclass(unsendable)]
struct SpeexPreprocessor {
    state: *mut SpeexPreprocessState,
    echo_state: Option<*mut SpeexEchoState>,
    #[pyo3(get, set)]
    pub frame_size: usize,
    #[pyo3(get, set)]
    pub sampling_rate: usize,
}

#[pymethods]
impl SpeexPreprocessor {
    #[new]
    fn new(frame_size: usize, sampling_rate: usize) -> PyResult<Self> {
        unsafe {
            let state = speex_preprocess_state_init(frame_size as c_int, sampling_rate as c_int);

            if state.is_null() {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to initialize Speex preprocessor",
                ));
            }

            Ok(SpeexPreprocessor {
                state,
                echo_state: None,
                frame_size,
                sampling_rate,
            })
        }
    }

    /// Process the input audio data
    /// Returns a tuple containing the processed audio data and a boolean indicating if the input was detected as speech
    fn process<'py>(
        &mut self,
        py: Python<'py>,
        input: &Bound<'py, PyBytes>,
        echo: &Bound<'py, PyBytes>,
    ) -> PyResult<(Bound<'py, PyBytes>, bool)> {
        if self.state.is_null() {
            return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Speex preprocessor not initialized or already cleaned up",
            ));
        }

        let input_bytes: &[u8] = input.extract()?;
        let echo_bytes: &[u8] = echo.extract()?;

        if input_bytes.len() != self.frame_size * 2 {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Input length must be {} bytes ({} samples a 2 bytes) ({} bytes given)",
                self.frame_size * 2,
                self.frame_size,
                input_bytes.len()
            )));
        }

        // Create a copy of the input data that we'll modify
        let mut input_copy = input_bytes.to_vec();

        // Safely cast bytes to i16 slice
        let samples = unsafe {
            slice::from_raw_parts_mut(input_copy.as_mut_ptr() as *mut i16, self.frame_size)
        };
        if let Some(echo_state) = self.echo_state {
            let echo_samples = unsafe {
                slice::from_raw_parts(echo_bytes.as_ptr() as *const i16, self.frame_size)
            };

            let mut output_buffer = vec![0i16; self.frame_size];

            unsafe {
                speex_echo_cancellation(
                    echo_state,
                    samples.as_ptr() as *mut i16,
                    echo_samples.as_ptr() as *mut i16,
                    output_buffer.as_mut_ptr(),
                );

                let samples_slice =
                    slice::from_raw_parts_mut(samples.as_mut_ptr(), self.frame_size);

                samples_slice.copy_from_slice(&output_buffer);
            }
        }

        // Process the audio
        // vad doesnt work in speex >= 1.2
        let vad = unsafe { speex_preprocess_run(self.state, samples.as_mut_ptr()) };
        // Return the modified copy as bytes
        Ok((PyBytes::new(py, &input_copy), vad != 0))
    }

    #[pyo3(signature = (supression_db))]
    fn set_denoise(&mut self, supression_db: Option<u8>) -> PyResult<()> {
        unsafe {
            let mut enabled = if supression_db.is_some() { 1 } else { 0 } as c_int;
            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_SET_DENOISE as c_int,
                &mut enabled as *mut _ as *mut c_void,
            );

            if ret != 0 {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to set denoise settings",
                ));
            }

            if let Some(supression_db) = supression_db {
                let mut supression = -(supression_db as i32);
                println!("Setting noise suppression level to {}", supression);
                let ret = speex_preprocess_ctl(
                    self.state,
                    SPEEX_PREPROCESS_SET_NOISE_SUPPRESS as c_int,
                    &mut supression as *mut _ as *mut c_void,
                );

                if ret != 0 {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Failed to set noise suppression level",
                    ));
                }
            }
        }
        Ok(())
    }

    #[pyo3(signature = (filter_length))]
    fn set_echo(&mut self, filter_length: i32) -> PyResult<()> {
        unsafe {
            let raw_echo_state =
                speex_echo_state_init(self.frame_size as c_int, filter_length as c_int);
            if raw_echo_state.is_null() {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to initialize Speex echo state",
                ));
            }

            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_SET_ECHO_STATE as c_int,
                raw_echo_state as *mut _ as *mut c_void,
            );

            if ret != 0 {
                // Clean up the echo state to avoid memory leak
                speex_echo_state_destroy(raw_echo_state);
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to set echo state",
                ));
            }

            self.echo_state = Some(raw_echo_state);
        }
        Ok(())
    }
    #[pyo3(signature = (enabled, level = None, increment = None, decrement = None, max_gain = None))]
    fn set_agc(
        &mut self,
        enabled: bool,
        level: Option<u16>,
        increment: Option<i32>,
        decrement: Option<i32>,
        max_gain: Option<i32>,
    ) -> PyResult<()> {
        unsafe {
            let mut enabled_val = if enabled { 1 } else { 0 } as c_int;
            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_SET_AGC as c_int,
                &mut enabled_val as *mut _ as *mut c_void,
            );

            if ret != 0 {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to set AGC settings",
                ));
            }

            // If AGC is enabled and level is provided, set the level
            if enabled && level.is_some() {
                let agc_level = level.unwrap();

                // For AGC level, we need to use a float value
                let mut level_float = agc_level as f32;
                println!("Setting AGC level to {}", level_float);

                let ret = speex_preprocess_ctl(
                    self.state,
                    SPEEX_PREPROCESS_SET_AGC_LEVEL as c_int,
                    &mut level_float as *mut _ as *mut c_void,
                );

                if ret != 0 {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Failed to set AGC level",
                    ));
                }
            }

            // Set AGC increment (how fast the gain can increase)
            if let Some(inc) = increment {
                let mut inc_val = inc as c_int;
                println!("Setting AGC increment to {}", inc_val);
                let ret = speex_preprocess_ctl(
                    self.state,
                    SPEEX_PREPROCESS_SET_AGC_INCREMENT as c_int,
                    &mut inc_val as *mut _ as *mut c_void,
                );

                if ret != 0 {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Failed to set AGC increment",
                    ));
                }
            }

            // Set AGC decrement (how fast the gain can decrease)
            if let Some(dec) = decrement {
                let mut dec_val = dec as c_int;
                println!("Setting AGC decrement to {}", dec_val);
                let ret = speex_preprocess_ctl(
                    self.state,
                    SPEEX_PREPROCESS_SET_AGC_DECREMENT as c_int,
                    &mut dec_val as *mut _ as *mut c_void,
                );

                if ret != 0 {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Failed to set AGC decrement",
                    ));
                }
            }

            // Set AGC maximum gain
            if let Some(gain) = max_gain {
                let mut gain_val = gain as c_int;
                println!("Setting AGC max gain to {}", gain_val);
                let ret = speex_preprocess_ctl(
                    self.state,
                    SPEEX_PREPROCESS_SET_AGC_MAX_GAIN as c_int,
                    &mut gain_val as *mut _ as *mut c_void,
                );

                if ret != 0 {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Failed to set AGC max gain",
                    ));
                }
            }
        }
        Ok(())
    }

    /// Get the current AGC (Automatic Gain Control) settings
    /// Returns None if AGC is disabled, or Some(level) with the current level if enabled
    fn get_agc(&self) -> PyResult<Option<u16>> {
        unsafe {
            // First check if AGC is enabled
            let mut enabled: c_int = 0;
            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_GET_AGC as c_int,
                &mut enabled as *mut _ as *mut c_void,
            );

            if ret != 0 {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to get AGC settings",
                ));
            }

            // If AGC is disabled, return None
            if enabled == 0 {
                return Ok(None);
            }

            // AGC is enabled, get the level (as a float)
            let mut level: f32 = 0.0;
            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_GET_AGC_LEVEL as c_int,
                &mut level as *mut _ as *mut c_void,
            );

            if ret != 0 {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to get AGC level",
                ));
            }

            Ok(Some(level as u16))
        }
    }

    /// Get the current noise suppression settings
    /// Returns None if noise suppression is disabled, or Some(level) with the current level in dB if enabled
    fn get_denoise(&self) -> PyResult<Option<i32>> {
        unsafe {
            // First check if denoise is enabled
            let mut enabled: c_int = 0;
            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_GET_DENOISE as c_int,
                &mut enabled as *mut _ as *mut c_void,
            );

            if ret != 0 {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to get denoise settings",
                ));
            }

            // If denoise is disabled, return None
            if enabled == 0 {
                return Ok(None);
            }

            // Denoise is enabled, get the suppression level
            let mut level: c_int = 0;
            let ret = speex_preprocess_ctl(
                self.state,
                SPEEX_PREPROCESS_GET_NOISE_SUPPRESS as c_int,
                &mut level as *mut _ as *mut c_void,
            );

            if ret != 0 {
                return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "Failed to get noise suppression level",
                ));
            }

            // The level is stored as a negative value, but we return the positive value
            // to be consistent with the set_denoise method
            Ok(Some(-level))
        }
    }

    fn cleanup(&mut self) {
        unsafe {
            if !self.state.is_null() {
                speex_preprocess_state_destroy(self.state);
            }

            if let Some(echo_state) = self.echo_state {
                if !echo_state.is_null() {
                    speex_echo_state_destroy(echo_state);
                }
            }
        }
    }
}

impl Drop for SpeexPreprocessor {
    fn drop(&mut self) {
        if !self.state.is_null() {
            println!(
                "Dropping initialized Speex preprocessor, consider calling cleanup() manually"
            );
        }
        self.cleanup();
    }
}

/// Returns the version of the speex-py wrapper
#[pyfunction]
fn version() -> PyResult<String> {
    Ok(format!(
        "0.1.1 (built on {})",
        env!("CARGO_BUILD_TIME", "unknown build time")
    ))
}

/// A Python module implemented in Rust.
#[pymodule]
fn speex_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SpeexPreprocessor>()?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
