CREATE TABLE dwd_zrr_gsrdxx_new (
    zrrwybs VARCHAR(320),
    sfzjlx VARCHAR(12),
    sfzjhm VARCHAR(320),
    xm VARCHAR(60),
    xb VARCHAR(6),
    sshbw TEXT,
    yrdw VARCHAR(200),
    tyshxydm VARCHAR(30),
    gsfssj VARCHAR(20),
    gsrdsqrq DATE,
    rdsqrygszggx TEXT,
    gsrdrq VARCHAR(20),
    gsrdjl TEXT,
    rdyjlb VARCHAR(100),
    sssdzygz VARCHAR(500),
    sglb VARCHAR(100),
    shcd TEXT,
    zybmc VARCHAR(200),
    jczybwhys NUMERIC
);

COMMENT ON TABLE dwd_zrr_gsrdxx_new IS '工伤认定信息表';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.xm IS '姓名';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.xb IS '性别';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.sshbw IS '受伤害部位';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.yrdw IS '用人单位';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.tyshxydm IS '统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.gsfssj IS '工伤发生时间';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.gsrdsqrq IS '工伤认定申请日期';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.rdsqrygszggx IS '认定申请人与工伤职工关系';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.gsrdrq IS '工伤认定日期';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.gsrdjl IS '工伤认定结论';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.rdyjlb IS '认定依据类别';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.sssdzygz IS '受伤时的职业工种';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.sglb IS '事故类别';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.shcd IS '伤害程度';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.zybmc IS '职业病名称';
COMMENT ON COLUMN dwd_zrr_gsrdxx_new.jczybwhys IS '接触职业病危害月数';