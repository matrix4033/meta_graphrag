CREATE TABLE dwd_zrr_jdcxx_new (
    zrrwybs VARCHAR(800),
    clsbdm VARCHAR(200),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    clgchjk CHAR(8),
    clzwpp VARCHAR(800),
    clxh VARCHAR(256),
    cllx VARCHAR(160),
    xszyxqz DATE
);

COMMENT ON TABLE dwd_zrr_jdcxx_new IS '机动车信息';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.clsbdm IS '车辆识别代码';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.clgchjk IS '车辆国产或进口';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.clzwpp IS '车辆中文品牌';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.clxh IS '车辆型号';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.cllx IS '车辆类型';
COMMENT ON COLUMN dwd_zrr_jdcxx_new.xszyxqz IS '行驶证有效期至';