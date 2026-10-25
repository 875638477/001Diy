source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
set created [::C12::CreateQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610.olb} QMI8610_C12 HOST_I2C]
set readback [::C12::ReadQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610.olb} QMI8610_C12 {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c12_reopen} HOST_I2C]
dict create created $created readback $readback
