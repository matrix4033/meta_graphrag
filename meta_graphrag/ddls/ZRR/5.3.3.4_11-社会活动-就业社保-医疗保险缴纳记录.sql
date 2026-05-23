CREATE TABLE dwd_zrr_yilbxjnjl_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    sbbm CHAR(144),
    sbxzlx CHAR(24),
    dwmc CHAR(144),
    dwtyshxydm CHAR(18),
    sbjfrq DATE,
    sbjfqsrq DATE,
    sbjfjzrq DATE,
    sbjfgz NUMERIC,
    sbjfjs NUMERIC,
    sbjfyf CHAR(48)
);

COMMENT ON TABLE dwd_zrr_yilbxjnjl_new IS '医疗保险缴纳记录';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbbm IS '社保编码';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbxzlx IS '社保险种类型';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.dwmc IS '单位名称';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.dwtyshxydm IS '单位统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbjfrq IS '社保缴费日期';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbjfqsrq IS '社保起始日期';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbjfjzrq IS '社保终止日期';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbjfgz IS '社保缴费工资';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbjfjs IS '社保缴费基数';
COMMENT ON COLUMN dwd_zrr_yilbxjnjl_new.sbjfyf IS '社保缴费月份';