CREATE TABLE dwd_zrr_hyxx_new (
    nfzrrwybs VARCHAR(800),
    nvfzrrwybs VARCHAR(800),
    jlhzzh CHAR(400),
    nfhyzk CHAR(16),
    nvfhyzk CHAR(16),
    djrq DATE,
    nfxm VARCHAR(800),
    nfsfzjlx CHAR(16),
    nfsfsfzjhm VARCHAR(400),
    nvfxm VARCHAR(800),
    nvfsfzjlx CHAR(16),
    nvfsfsfzjhm VARCHAR(400),
    birth_man DATE,
    birth_woman DATE,
    id_type_man VARCHAR(800),
    id_type_woman VARCHAR(800),
    nation_man VARCHAR(240),
    nation_woman VARCHAR(240),
    folk_man VARCHAR(4000),
    folk_woman VARCHAR(800),
    print_num_man CHAR(16),
    print_num_woman CHAR(16),
    lhpjah VARCHAR(200),
    jarq DATE,
    hydjlx VARCHAR(255)
);

COMMENT ON TABLE dwd_zrr_hyxx_new IS '婚姻信息';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nfzrrwybs IS '男方自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nvfzrrwybs IS '女方自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_hyxx_new.jlhzzh IS '结离婚证字号';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nfhyzk IS '婚姻状况(男)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nvfhyzk IS '婚姻状况(女)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.djrq IS '登记日期';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nfxm IS '男方姓名';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nfsfzjlx IS '男方身份证件类型';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nfsfsfzjhm IS '男方身份证件号码';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nvfxm IS '女方姓名';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nvfsfzjlx IS '女方身份证件类型';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nvfsfsfzjhm IS '女方身份证件号码';
COMMENT ON COLUMN dwd_zrr_hyxx_new.birth_man IS '出生日期(男)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.birth_woman IS '出生日期(女)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.id_type_man IS '身份类别(男)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.id_type_woman IS '身份类别(女)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nation_man IS '国籍(男)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.nation_woman IS '国籍(女)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.folk_man IS '民族(男)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.folk_woman IS '民族(女)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.print_num_man IS '印制号(男)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.print_num_woman IS '印制号(女)';
COMMENT ON COLUMN dwd_zrr_hyxx_new.lhpjah IS '离婚判决案号';
COMMENT ON COLUMN dwd_zrr_hyxx_new.jarq IS '结案日期';
COMMENT ON COLUMN dwd_zrr_hyxx_new.hydjlx IS '婚姻登记类型';