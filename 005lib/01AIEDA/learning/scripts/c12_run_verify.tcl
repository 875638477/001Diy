source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
set i2c [::C12::ReadQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610.olb} QMI8610_C12 {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c12_i2c_verified} HOST_I2C]
set flags [::C12::ProbePowerFlags {D:/001DIY/005lib/01AIEDA/learning/staging/capture_C_20261019/c12_power_flags_probe.olb} {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c12_power_flags_probe.tsv}]
set spi [::C12::CreateQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610_spi4.olb} QMI8610_C12_SPI4 HOST_SPI4]
set spiRead [::C12::ReadQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610_spi4.olb} QMI8610_C12_SPI4 {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c12_spi4_verified} HOST_SPI4]
dict create i2c $i2c flags $flags spi $spiRead
