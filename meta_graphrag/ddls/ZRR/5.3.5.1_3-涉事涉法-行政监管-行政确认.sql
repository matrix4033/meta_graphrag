CREATE TABLE dwd_zrr_xzqr_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    xzqrlb VARCHAR(800),
    xzqrws VARCHAR(800),
    xzqrrq DATE
);

COMMENT ON TABLE dwd_zrr_xzqr_new IS '行政确认';
COMMENT ON COLUMN dwd_zrr_xzqr_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzqr_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzqr_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzqr_new.xzqrlb IS '行政确认类别';
COMMENT ON COLUMN dwd_zrr_xzqr_new.xzqrws IS '行政确认文书号';
COMMENT ON COLUMN dwd_zrr_xzqr_new.xzqrrq IS '行政确认日期';