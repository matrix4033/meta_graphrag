CREATE TABLE dwd_zrr_sybxxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    shbzhm VARCHAR(200),
    dwmc VARCHAR(200),
    dwtyshxydm VARCHAR(200),
    cbdxzqhdm VARCHAR(100),
    cbksrq DATE,
    sbcbzt VARCHAR(200),
    sbzzrq DATE,
    zhjlny VARCHAR(100),
    zjfs VARCHAR(100),
    ygxs VARCHAR(100),
    grjfzt CHAR(50),
    cbsf VARCHAR(100),
    dfcbsfmz CHAR(50),
    dfcbsfmc VARCHAR(100),
    ldgxksrq DATE,
    ldgxzzrq DATE,
    dqyxbz CHAR(50),
    rycbgxlx VARCHAR(100),
    jfrylb CHAR(50),
    grcbrq DATE
);

COMMENT ON TABLE dwd_zrr_sybxxx_new IS '生育保险信息';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.shbzhm IS '社会保障号码';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.dwmc IS '单位名称';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.dwtyshxydm IS '单位统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.cbdxzqhdm IS '参保地行政区划代码';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.cbksrq IS '参保开始日期';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.sbcbzt IS '社保参保状态';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.sbzzrq IS '社保终止日期';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.zhjlny IS '账户建立年月';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.zjfs IS '征缴方式';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.ygxs IS '用工形式';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.grjfzt IS '个人缴费状态';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.cbsf IS '参保身份';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.dfcbsfmz IS '地方参保身份码值';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.dfcbsfmc IS '地方参保身份名称';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.ldgxksrq IS '劳动关系开始日期';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.ldgxzzrq IS '劳动关系终止日期';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.dqyxbz IS '当前有效标志';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.rycbgxlx IS '人员参保关系类型';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.jfrylb IS '缴费人员类别';
COMMENT ON COLUMN dwd_zrr_sybxxx_new.grcbrq IS '个人参保日期';