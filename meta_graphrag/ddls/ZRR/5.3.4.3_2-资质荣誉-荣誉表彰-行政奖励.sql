CREATE TABLE dwd_zrr_xzjl_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    xzjljdwh VARCHAR(2000),
    xzjlmc VARCHAR(1000),
    xzjljdnr VARCHAR(2000),
    xzjlrq DATE,
    xzjlbm VARCHAR(200),
    sjdj VARCHAR(100),
    xmmc CHAR(300),
    sbnd DATE,
    kssj DATE,
    jssj DATE,
    jllx CHAR(300)
);

COMMENT ON TABLE dwd_zrr_xzjl_new IS '行政奖励';
COMMENT ON COLUMN dwd_zrr_xzjl_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzjl_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzjl_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzjl_new.xzjljdwh IS '行政奖励决定文号';
COMMENT ON COLUMN dwd_zrr_xzjl_new.xzjlmc IS '行政奖励名称';
COMMENT ON COLUMN dwd_zrr_xzjl_new.xzjljdnr IS '行政奖励决定内容';
COMMENT ON COLUMN dwd_zrr_xzjl_new.xzjlrq IS '行政奖励日期';
COMMENT ON COLUMN dwd_zrr_xzjl_new.xzjlbm IS '行政奖励部门';
COMMENT ON COLUMN dwd_zrr_xzjl_new.sjdj IS '授奖等级';
COMMENT ON COLUMN dwd_zrr_xzjl_new.xmmc IS '项目名称';
COMMENT ON COLUMN dwd_zrr_xzjl_new.sbnd IS '年度';
COMMENT ON COLUMN dwd_zrr_xzjl_new.kssj IS '开始时间';
COMMENT ON COLUMN dwd_zrr_xzjl_new.jssj IS '结束时间';
COMMENT ON COLUMN dwd_zrr_xzjl_new.jllx IS '奖励类型';