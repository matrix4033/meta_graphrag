CREATE TABLE dwd_zrr_szbzjxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    szbzje NUMERIC,
    szbzlx CHAR(8)
);

COMMENT ON TABLE dwd_zrr_szbzjxx_new IS '丧葬补助金信息';
COMMENT ON COLUMN dwd_zrr_szbzjxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_szbzjxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_szbzjxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_szbzjxx_new.szbzje IS '丧葬补助金额';
COMMENT ON COLUMN dwd_zrr_szbzjxx_new.szbzlx IS '丧葬补助类型';