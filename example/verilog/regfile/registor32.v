

module registor32(
    input EN,
    input clk,
    input [31:0] D,
    output [31:0] Q
);

DFF d0(D[0], EN, clk, Q[0]);
DFF d1(D[1], EN, clk, Q[1]);
DFF d2(D[2], EN, clk, Q[2]);
DFF d3(D[3], EN, clk, Q[3]);
DFF d4(D[4], EN, clk, Q[4]);
DFF d5(D[5], EN, clk, Q[5]);
DFF d6(D[6], EN, clk, Q[6]);
DFF d7(D[7], EN, clk, Q[7]);
DFF d8(D[8], EN, clk, Q[8]);
DFF d9(D[9], EN, clk, Q[9]);
DFF d10(D[10], EN, clk, Q[10]);
DFF d11(D[11], EN, clk, Q[11]);
DFF d12(D[12], EN, clk, Q[12]);
DFF d13(D[13], EN, clk, Q[13]);
DFF d14(D[14], EN, clk, Q[14]);
DFF d15(D[15], EN, clk, Q[15]);
DFF d16(D[16], EN, clk, Q[16]);
DFF d17(D[17], EN, clk, Q[17]);
DFF d18(D[18], EN, clk, Q[18]);
DFF d19(D[19], EN, clk, Q[19]);
DFF d20(D[20], EN, clk, Q[20]);
DFF d21(D[21], EN, clk, Q[21]);
DFF d22(D[22], EN, clk, Q[22]);
DFF d23(D[23], EN, clk, Q[23]);
DFF d24(D[24], EN, clk, Q[24]);
DFF d25(D[25], EN, clk, Q[25]);
DFF d26(D[26], EN, clk, Q[26]);
DFF d27(D[27], EN, clk, Q[27]);
DFF d28(D[28], EN, clk, Q[28]);
DFF d29(D[29], EN, clk, Q[29]);
DFF d30(D[30], EN, clk, Q[30]);
DFF d31(D[31], EN, clk, Q[31]);

endmodule

module DFF(
    input D,
    input EN,
    input clk,
    output reg Q
);
reg out;

always @(posedge clk)
begin
  out = (EN) ? D : Q;
  Q = out;
end

endmodule