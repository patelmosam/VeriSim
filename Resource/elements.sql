PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Elements" (
	"name" text, "file_path" text, "category" text
);
INSERT INTO Elements VALUES('And','components/gates/and.v','Gates');
INSERT INTO Elements VALUES('Or','components/gates/or.v','Gates');
INSERT INTO Elements VALUES('Not','components/gates/not.v','Gates');
INSERT INTO Elements VALUES('Input','','Inputs');
INSERT INTO Elements VALUES('Monitor','','Outputs');
INSERT INTO Elements VALUES('Mux_2_1','components/mux/mux_2_1.v','Mux');
COMMIT;