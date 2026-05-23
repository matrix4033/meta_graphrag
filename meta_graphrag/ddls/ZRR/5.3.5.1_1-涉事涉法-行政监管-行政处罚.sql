CREATE TABLE dwd_zrr_xzcf_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    xzcfdxszzzjgtyshxydm CHAR(144),
    xzcfdxszzzjgdm VARCHAR(240),
    xzcfzl CHAR(40),
    xzwfxwlx VARCHAR(320),
    xzcfjdswh VARCHAR(800),
    xzcfnr VARCHAR(16000),
    xzcfjd VARCHAR(8000),
    xzcfyj VARCHAR(16000),
    xzcfrq DATE,
    xzcfjkbj VARCHAR(800),
    xzcfnx VARCHAR(400),
    xzcfjg VARCHAR(800),
    xzcfjgbhxzcfjgbh VARCHAR(800),
    xzcfbmjb VARCHAR(160),
    blxwdjrq DATE,
    xzwfxwfsrq DATE
);

COMMENT ON TABLE dwd_zrr_xzcf_new IS '行政处罚';
COMMENT ON COLUMN dwd_zrr_xzcf_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzcf_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzcf_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfdxszzzjgtyshxydm IS '行政处罚对象所在组织机构统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfdxszzzjgdm IS '行政处罚对象所在组织机构代码';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfzl IS '行政处罚种类';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzwfxwlx IS '行政违法行为类型';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfjdswh IS '行政处罚决定书文号';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfnr IS '行政处罚内容';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfjd IS '行政处罚决定';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfyj IS '行政处罚依据';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfrq IS '行政处罚日期';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfjkbj IS '行政处罚交款标记';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfnx IS '行政处罚年限';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfjg IS '行政处罚机关';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfjgbhxzcfjgbh IS '行政处罚机构编号(行政处罚机关编号)';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzcfbmjb IS '行政处罚部门级别';
COMMENT ON COLUMN dwd_zrr_xzcf_new.blxwdjrq IS '不良行为登记日期';
COMMENT ON COLUMN dwd_zrr_xzcf_new.xzwfxwfsrq IS '行政违法行为发生日期';