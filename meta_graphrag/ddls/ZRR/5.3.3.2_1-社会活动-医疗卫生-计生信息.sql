CREATE TABLE dwd_zrr_jsxx_new (
    zrrwybs VARCHAR(1381),
    sfzjlx VARCHAR(1381),
    sfzjhm VARCHAR(1381),
    yljgmc VARCHAR(100),
    cfjkdah VARCHAR(20),
    cfzybah VARCHAR(40),
    jdsj DATE,
    gwrs VARCHAR(5),
    rsbfz VARCHAR(200),
    rsfxdm VARCHAR(10),
    cfyc VARCHAR(200),
    cfcc VARCHAR(200),
    cfts VARCHAR(200),
    cftc VARCHAR(200)
);

COMMENT ON TABLE dwd_zrr_jsxx_new IS '计生信息';
COMMENT ON COLUMN dwd_zrr_jsxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jsxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jsxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jsxx_new.yljgmc IS '医疗机构名称';
COMMENT ON COLUMN dwd_zrr_jsxx_new.cfjkdah IS '孕产妇健康档案编号';
COMMENT ON COLUMN dwd_zrr_jsxx_new.cfzybah IS '产妇住院病案号';
COMMENT ON COLUMN dwd_zrr_jsxx_new.jdsj IS '建档时间';
COMMENT ON COLUMN dwd_zrr_jsxx_new.gwrs IS '本次是否属于高危妊娠';
COMMENT ON COLUMN dwd_zrr_jsxx_new.rsbfz IS '妊娠合并症/并发症史';
COMMENT ON COLUMN dwd_zrr_jsxx_new.rsfxdm IS '妊娠风险评估分级代码';
COMMENT ON COLUMN dwd_zrr_jsxx_new.cfyc IS '孕次（次）';
COMMENT ON COLUMN dwd_zrr_jsxx_new.cfcc IS '产次（次）';
COMMENT ON COLUMN dwd_zrr_jsxx_new.cfts IS '胎数';
COMMENT ON COLUMN dwd_zrr_jsxx_new.cftc IS '胎次';