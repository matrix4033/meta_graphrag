CREATE TABLE dwd_zrr_jtcx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    cfsj DATE,
    ddsj DATE,
    sfzmc VARCHAR(800),
    sfzdm VARCHAR(800),
    ddzmc VARCHAR(800),
    ddzdm VARCHAR(800),
    xlmc VARCHAR(800),
    gpsj TIMESTAMP,
    gxsj TIMESTAMP
);

COMMENT ON TABLE dwd_zrr_jtcx_new IS '交通出行';
COMMENT ON COLUMN dwd_zrr_jtcx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jtcx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jtcx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jtcx_new.cfsj IS '出发时间';
COMMENT ON COLUMN dwd_zrr_jtcx_new.ddsj IS '到达时间';
COMMENT ON COLUMN dwd_zrr_jtcx_new.sfzmc IS '始发站名称';
COMMENT ON COLUMN dwd_zrr_jtcx_new.sfzdm IS '始发站代码';
COMMENT ON COLUMN dwd_zrr_jtcx_new.ddzmc IS '到达站名称';
COMMENT ON COLUMN dwd_zrr_jtcx_new.ddzdm IS '到达站代码';
COMMENT ON COLUMN dwd_zrr_jtcx_new.xlmc IS '线路名称';
COMMENT ON COLUMN dwd_zrr_jtcx_new.gpsj IS '购票时间';
COMMENT ON COLUMN dwd_zrr_jtcx_new.gxsj IS '更新时间';