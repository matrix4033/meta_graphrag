CREATE TABLE dwd_zrr_jdcjszjbxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx VARCHAR(10),
    sfzjhm VARCHAR(800),
    sjhm VARCHAR(400),
    zjcx VARCHAR(400),
    bldz VARCHAR(400),
    cclzrq DATE,
    yxqs DATE,
    yxqz DATE
);

COMMENT ON TABLE dwd_zrr_jdcjszjbxx_new IS '机动车驾驶证基本信息';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.sjhm IS '手机号码';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.zjcx IS '准驾车型';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.bldz IS '办理地址';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.cclzrq IS '初次领证日期';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.yxqs IS '有效期始';
COMMENT ON COLUMN dwd_zrr_jdcjszjbxx_new.yxqz IS '有效期止';