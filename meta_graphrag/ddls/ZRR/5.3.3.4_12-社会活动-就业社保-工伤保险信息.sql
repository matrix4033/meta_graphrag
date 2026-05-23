CREATE TABLE dwd_zrr_gsbxxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx VARCHAR(50),
    sfzjhm VARCHAR(200),
    shbzhm VARCHAR(200),
    dwmc VARCHAR(200),
    dwtyshxydm VARCHAR(200),
    cbdxzqhdm VARCHAR(100),
    cbksrq VARCHAR(50),
    bcjfksny VARCHAR(50),
    sbcbzt VARCHAR(200),
    sbzzrq VARCHAR(50),
    zhjlny VARCHAR(100),
    zjfs VARCHAR(100),
    ygxs VARCHAR(100),
    grjfzt VARCHAR(50),
    cbsf VARCHAR(100),
    dfcbsfmz VARCHAR(50),
    dfcbsfmc VARCHAR(100),
    ldgxksrq DATE,
    ldgxzzrq DATE,
    dqyxbz VARCHAR(50),
    rycbgxlx VARCHAR(100),
    jfrylb VARCHAR(50),
    grcbrq VARCHAR(50)
);

COMMENT ON TABLE dwd_zrr_gsbxxx_new IS '工伤保险信息';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.shbzhm IS '社会保障号码';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.dwmc IS '单位名称';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.dwtyshxydm IS '单位统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.cbdxzqhdm IS '参保所属地';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.cbksrq IS '参保开始日期';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.bcjfksny IS '本次缴费开始年月';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.sbcbzt IS '社保参保状态';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.sbzzrq IS '社保终止日期';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.zhjlny IS '账户建立年月';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.zjfs IS '征缴方式';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.ygxs IS '用工形式';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.grjfzt IS '个人缴费状态';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.cbsf IS '参保身份';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.dfcbsfmz IS '地方参保身份码值';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.dfcbsfmc IS '地方参保身份名称';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.ldgxksrq IS '劳动关系开始日期';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.ldgxzzrq IS '劳动关系终止日期';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.dqyxbz IS '当前有效标志';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.rycbgxlx IS '人员参保关系类型';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.jfrylb IS '缴费人员类别';
COMMENT ON COLUMN dwd_zrr_gsbxxx_new.grcbrq IS '个人参保日期';