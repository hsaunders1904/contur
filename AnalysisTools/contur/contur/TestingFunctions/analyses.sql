PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE analysis_pool (
    pool    TEXT NOT NULL UNIQUE,
    PRIMARY KEY(pool)
);
INSERT INTO analysis_pool VALUES('ATLAS_7_JETS');    -- 0
INSERT INTO analysis_pool VALUES('ATLAS_7_Zjj_EL');  -- 1
INSERT INTO analysis_pool VALUES('ATLAS_7_Wjj_mu');  -- 2
INSERT INTO analysis_pool VALUES('CMS_7_JETS');      -- 3
INSERT INTO analysis_pool VALUES('CMS_7_Wjj');       -- 4
INSERT INTO analysis_pool VALUES('CMS_7_Zjj');       -- 5
INSERT INTO analysis_pool VALUES('ATLAS_8_JETS');    -- 6
INSERT INTO analysis_pool VALUES('ATLAS_7_Wjj_EL');  -- 7
INSERT INTO analysis_pool VALUES('ATLAS_7_GAMMA');   -- 8
INSERT INTO analysis_pool VALUES('ATLAS_7_Z_GAMMA');
INSERT INTO analysis_pool VALUES('ATLAS_7_W_GAMMA_MU'); -- 10
INSERT INTO analysis_pool VALUES('ATLAS_7_W_GAMMA_EL');
INSERT INTO analysis_pool VALUES('ATLAS_7_ZZ');         -- 12
INSERT INTO analysis_pool VALUES('ATLAS_7_GAMMAGAMMA');
INSERT INTO analysis_pool VALUES('CMS_GAMMA_JET');      -- 14
INSERT INTO analysis_pool VALUES('ATLAS_7_Zjj_MU');
INSERT INTO analysis_pool VALUES('ATLAS_8_Zjj');        -- 16
INSERT INTO analysis_pool VALUES('ATLAS_8_GAMMA');      -- 17
CREATE TABLE analysis (
    id      TEXT NOT NULL UNIQUE,
    lumi    REAL NOT NULL,
    pool    TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(pool) REFERENCES analysis_pool(pool)
);
INSERT INTO analysis VALUES('ATLAS_2014_I1325553',4500.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2014_I1268975',4500.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2014_I1326641',4510.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2013_I1230812_EL',4600.0,'ATLAS_7_Zjj_EL');
INSERT INTO analysis VALUES('ATLAS_2012_I1093738',37.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2012_I1083318',36.0,NULL);
INSERT INTO analysis VALUES('ATLAS_2011_I945498',36.0,NULL);
INSERT INTO analysis VALUES('ATLAS_2011_I921594',35.0,NULL);
INSERT INTO analysis VALUES('ATLAS_2011_S9128077',2.4,NULL);
INSERT INTO analysis VALUES('CMS_2014_I1298810',5000.0,'CMS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2013_I1244522',37.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2014_I1306294_EL',4600.0,'ATLAS_7_Zjj_EL');
-- commented out in python 'CMS_2013_I1256943',5200.0
INSERT INTO analysis VALUES('CMS_2015_I1310737',4900.0,'CMS_7_Zjj');
INSERT INTO analysis VALUES('CMS_2014_I1303894',5000.0,'CMS_7_Wjj');
INSERT INTO analysis VALUES('ATLAS_2014_I1319490_MU',4600.0,'ATLAS_7_Wjj_mu');
INSERT INTO analysis VALUES('ATLAS_2014_I1319490_EL',4600.0,'ATLAS_7_Wjj_EL');
INSERT INTO analysis VALUES('ATLAS_2015_I1394679',20.3,'ATLAS_8_JETS');
INSERT INTO analysis VALUES('ATLAS_2014_I1307243',4500.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2013_I1263495',4600.0,'ATLAS_7_GAMMA');

INSERT INTO analysis VALUES('ATLAS_2013_I1217863_Z',4.6,'ATLAS_7_Z_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_W_MU',4.6,'ATLAS_7_W_GAMMA_MU');
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_W_EL',4.6,'ATLAS_7_W_GAMMA_EL');
INSERT INTO analysis VALUES('ATLAS_2012_I1203852',4.6,'ATLAS_7_ZZ');
INSERT INTO analysis VALUES('ATLAS_2012_I1199269',4900.0,'ATLAS_7_GAMMAGAMMA');
INSERT INTO analysis VALUES('CMS_2014_I1266056',4500.0,'CMS_GAMMA_JET');
INSERT INTO analysis VALUES('ATLAS_2014_I1306294_MU',4600.0,'ATLAS_7_Zjj_MU');
INSERT INTO analysis VALUES('ATLAS_2013_I1230812_MU',4600.0,'ATLAS_7_Zjj_MU');
-- commented out in python 'CMS_2013_I1224539_WJET',5000.0,CMS_7_Wjj
-- commented out in python 'CMS_2013_I1224539_ZJET',5000.0,CMS_7_Zjj
INSERT INTO analysis VALUES('ATLAS_2014_I1279489',20300.0,'ATLAS_8_Zjj');
INSERT INTO analysis VALUES('ATLAS_2015_I1408516',20300.0,'ATLAS_8_Zjj');
INSERT INTO analysis VALUES('ATLAS_2016_I1457605',20200.0,'ATLAS_8_GAMMA');


CREATE TABLE blacklist (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d02');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d04');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d06');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d08');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d02');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d04');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d06');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d08');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d13');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d14');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d15');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d16');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d17');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d18');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_Z','d17');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_Z','d18');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_Z','d20');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_MU','d15');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_MU','d16');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_MU','d19');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_EL','d15');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_EL','d16');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_EL','d19');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d03');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d04');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d05');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d06');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d07');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d08');
INSERT INTO blacklist VALUES('ATLAS_2012_I1199269','d04');



CREATE TABLE whitelist (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d01-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d01-x02-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d02-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d03-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d03-x02-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d04-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d04-x02-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d05-x03-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d05-x04-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d05-x05-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d13');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d14');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d15');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d16');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d17');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d18');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d19');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d20');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d21');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d22');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d23');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d24');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d25');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d26');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d27');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d28');


CREATE TABLE subpool (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    subid   INTEGER NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO subpool VALUES('ATLAS_2014_I1325553','d01-x01-y0[1-6]',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1325553','d02-x01-y0[1-6]',1);
INSERT INTO subpool VALUES('ATLAS_2014_I1268975','d01-x01-y0[1-6]',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1268975','d02-x01-y0[1-6]',1);
INSERT INTO subpool VALUES('ATLAS_2014_I1326641','d0[1-5]-x01-y01',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1326641','(d10|d0[6-9])-x01-y01',1);
INSERT INTO subpool VALUES('CMS_2014_I1298810','d0[1-6]-x01-y01',0);
-- check this next one, one of the .py entries had y02 listed
INSERT INTO subpool VALUES('CMS_2014_I1298810','(d1[0-2]|d0[7-9])-x01-y01',1);
INSERT INTO subpool VALUES('ATLAS_2014_I1307243','(d20|d1[3-9])-x01-y01',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1307243','d2[1-8]-x01-y01',1);
INSERT INTO subpool VALUES('ATLAS_2013_I1263495','d01-x01-y0[13]',0);


INSERT INTO subpool VALUES('ATLAS_2016_I1457605','.',0);

CREATE TABLE normalization (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    norm    REAL NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d01',5.88);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d02',1.82);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d05',0.066);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d03',1.10);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d04',0.447);
;
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d23',1.45);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d24',1.03);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d25',0.97);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d02',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d03',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d04',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d14',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d26',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d05',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d06',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d07',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d08',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d09',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d10',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d15',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d17',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d18',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d19',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d20',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d21',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d22',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d27',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d11',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d12',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d13',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d16',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d28',5.59);
COMMIT;
