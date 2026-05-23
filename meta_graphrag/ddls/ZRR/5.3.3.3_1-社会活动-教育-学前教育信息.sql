CREATE TABLE dwd_zrr_xqjyxx_new (
    zrrwybs VARCHAR(800),
    sfzjhm VARCHAR(800),
    sfzjlx CHAR(16),
    xxwybs VARCHAR(800),
    xxmc VARCHAR(800),
    rxrq DATE,
    byrq DATE,
    bjmc VARCHAR(400)
);

COMMENT ON TABLE dwd_zrr_xqjyxx_new IS '学前教育信息';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.xxwybs IS '学校唯一标识';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.xxmc IS '学校名称';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.rxrq IS '入学日期';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.byrq IS '毕业日期';
COMMENT ON COLUMN dwd_zrr_xqjyxx_new.bjmc IS '班级名称';