CREATE TABLE dwd_zrr_xzcj_new (
    xzcfje NUMERIC,
    xzcfsfxxgk CHAR(8),
    xzcfgksj DATE,
    xzcfgkjssj DATE,
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    xzcjbsqr VARCHAR(1000),
    xzcjsqsx VARCHAR(4000),
    xzcjssjg VARCHAR(1000),
    xzcjrq DATE
);

COMMENT ON TABLE dwd_zrr_xzcj_new IS '行政裁决';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcfje IS '行政处罚金额';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcfsfxxgk IS '行政处罚是否信息公开';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcfgksj IS '行政处罚公开时间';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcfgkjssj IS '行政处罚公开结束时间';
COMMENT ON COLUMN dwd_zrr_xzcj_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzcj_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzcj_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcjbsqr IS '行政裁决被申请人';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcjsqsx IS '行政裁决申请事项';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcjssjg IS '行政裁决实施机关';
COMMENT ON COLUMN dwd_zrr_xzcj_new.xzcjrq IS '行政裁决日期';