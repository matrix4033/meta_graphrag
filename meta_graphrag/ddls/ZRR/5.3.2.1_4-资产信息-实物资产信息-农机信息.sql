CREATE TABLE dwd_zrr_njxx_new (
    zrrwybs VARCHAR(800),
    njjjhm VARCHAR(2040),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    njjsscrs INTEGER,
    njlx VARCHAR(2040)
);

COMMENT ON TABLE dwd_zrr_njxx_new IS '农机信息';
COMMENT ON COLUMN dwd_zrr_njxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_njxx_new.njjjhm IS '农机机架号码';
COMMENT ON COLUMN dwd_zrr_njxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_njxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_njxx_new.njjsscrs IS '农机驾驶室乘人数';
COMMENT ON COLUMN dwd_zrr_njxx_new.njlx IS '农机类型';