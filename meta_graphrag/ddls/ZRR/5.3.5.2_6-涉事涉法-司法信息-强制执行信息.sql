CREATE TABLE dwd_zrr_qzzxxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    qzzxsqzxr VARCHAR(400),
    qzzxfydm VARCHAR(400),
    qzzxfymc VARCHAR(800),
    qzzxyjwsh VARCHAR(800),
    qzzxlasj DATE,
    zcqzzxyjdw VARCHAR(800),
    bqzzxrdlxqk VARCHAR(800),
    qzzxfbsj DATE
);

COMMENT ON TABLE dwd_zrr_qzzxxx_new IS '强制执行信息';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.qzzxsqzxr IS '强制执行申请执行人';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.qzzxfydm IS '强制执行法院代码';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.qzzxfymc IS '强制执行法院名称';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.qzzxyjwsh IS '强制执行依据文书号';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.qzzxlasj IS '强制执行立案时间';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.zcqzzxyjdw IS '做出强制执行依据单位';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.bqzzxrdlxqk IS '被强制执行人的履行情况';
COMMENT ON COLUMN dwd_zrr_qzzxxx_new.qzzxfbsj IS '强制执行发布时间';