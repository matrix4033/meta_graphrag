CREATE TABLE dwd_zrr_wthd_new (
    zrrwybs VARCHAR(1600),
    sfzjlx CHAR(128),
    sfzjhm VARCHAR(1600),
    hdmc VARCHAR(3000),
    zyzhdzsc DOUBLE PRECISION
);

COMMENT ON TABLE dwd_zrr_wthd_new IS '文体活动';
COMMENT ON COLUMN dwd_zrr_wthd_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_wthd_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_wthd_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_wthd_new.hdmc IS '活动名称';
COMMENT ON COLUMN dwd_zrr_wthd_new.zyzhdzsc IS '志愿者活动总时长';