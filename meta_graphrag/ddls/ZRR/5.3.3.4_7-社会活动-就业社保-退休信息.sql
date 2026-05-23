CREATE TABLE dwd_zrr_txxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx VARCHAR(20),
    sfzjhm VARCHAR(800),
    ltxzh VARCHAR(60),
    sqtxyy VARCHAR(1600),
    txsszdwmc VARCHAR(800),
    ltxzw VARCHAR(160),
    ltxrq DATE,
    ltxzje NUMERIC,
    ltxrylb VARCHAR(20),
    cjgmgzrq VARCHAR(20),
    fdltxrq DATE,
    ltxlb VARCHAR(60),
    dfltxlb VARCHAR(60),
    dfltxlbmc VARCHAR(100),
    dyxsksny VARCHAR(20),
    shhglxs VARCHAR(100),
    yctxbs VARCHAR(20),
    txtxbs VARCHAR(20),
    bcjtbs VARCHAR(20)
);

COMMENT ON TABLE dwd_zrr_txxx_new IS '退休信息';
COMMENT ON COLUMN dwd_zrr_txxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_txxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_txxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_txxx_new.ltxzh IS '离退休证号';
COMMENT ON COLUMN dwd_zrr_txxx_new.sqtxyy IS '申请退休原因';
COMMENT ON COLUMN dwd_zrr_txxx_new.txsszdwmc IS '退休时所在单位名称';
COMMENT ON COLUMN dwd_zrr_txxx_new.ltxzw IS '离退休职务';
COMMENT ON COLUMN dwd_zrr_txxx_new.ltxrq IS '离退休日期';
COMMENT ON COLUMN dwd_zrr_txxx_new.ltxzje IS '离退休金总额';
COMMENT ON COLUMN dwd_zrr_txxx_new.ltxrylb IS '离退休人员类别';
COMMENT ON COLUMN dwd_zrr_txxx_new.cjgmgzrq IS '参加革命工作日期';
COMMENT ON COLUMN dwd_zrr_txxx_new.fdltxrq IS '法定离退休日期';
COMMENT ON COLUMN dwd_zrr_txxx_new.ltxlb IS '离退休类别';
COMMENT ON COLUMN dwd_zrr_txxx_new.dfltxlb IS '地方离退休类别';
COMMENT ON COLUMN dwd_zrr_txxx_new.dfltxlbmc IS '地方离退休类别名称';
COMMENT ON COLUMN dwd_zrr_txxx_new.dyxsksny IS '待遇享受开始年月';
COMMENT ON COLUMN dwd_zrr_txxx_new.shhglxs IS '社会化管理形式';
COMMENT ON COLUMN dwd_zrr_txxx_new.yctxbs IS '延迟退休标识';
COMMENT ON COLUMN dwd_zrr_txxx_new.txtxbs IS '弹性退休标识';
COMMENT ON COLUMN dwd_zrr_txxx_new.bcjtbs IS '病残津贴标识';