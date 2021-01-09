PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Elements" (
	"name" text, "file_path" text, "category" text
);
INSERT INTO Elements VALUES('And','Resource/components/gates/and.v','Gates');
INSERT INTO Elements VALUES('Or','Resource/components/gates/or.v','Gates');
INSERT INTO Elements VALUES('Not','Resource/components/gates/not.v','Gates');
INSERT INTO Elements VALUES('Input','','Inputs');
INSERT INTO Elements VALUES('Monitor','','Outputs');
INSERT INTO Elements VALUES('Mux_2_1','Resource/components/mux/mux_2_1.v','Mux');
COMMIT;