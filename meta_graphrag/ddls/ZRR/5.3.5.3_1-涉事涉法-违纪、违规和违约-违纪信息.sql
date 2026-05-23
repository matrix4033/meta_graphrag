CREATE TABLE dwd_zrr_wjxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    wjlx CHAR(40),
    wjnr VARCHAR(16000),
    wjrszjgmc VARCHAR(800),
    wjclyj VARCHAR(8000)
);

COMMENT ON TABLE dwd_zrr_wjxx_new IS '违纪信息';
COMMENT ON COLUMN dwd_zrr_wjxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_wjxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_wjxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_wjxx_new.wjlx IS '违纪类型';
COMMENT ON COLUMN dwd_zrr_wjxx_new.wjnr IS '违纪内容';
COMMENT ON COLUMN dwd_zrr_wjxx_new.wjrszjgmc IS '违纪人所在机构名称';
COMMENT ON COLUMN dwd_zrr_wjxx_new.wjclyj IS '违纪处理意见';