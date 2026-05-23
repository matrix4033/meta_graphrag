CREATE TABLE dwd_zrr_sfzjxx_new (
    zrrwybs VARCHAR(1600),
    sfzjlx CHAR(400),
    sfzjhm VARCHAR(1600),
    sfzjyxq DATE,
    zjyxqqsrq DATE
);

COMMENT ON TABLE dwd_zrr_sfzjxx_new IS '身份证件信息';
COMMENT ON COLUMN dwd_zrr_sfzjxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_sfzjxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_sfzjxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_sfzjxx_new.sfzjyxq IS '身份证件有效期';
COMMENT ON COLUMN dwd_zrr_sfzjxx_new.zjyxqqsrq IS '证件有效期起始日期';