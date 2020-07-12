`include "and32.v"
`include "or32.v"
`include "nor32.v"
`include "xor32.v"
//`include "mux32_4_2.v"

module logic_unit(
    input [31:0] a,
    input [31:0] b,
    input [1:0] sel,
    output [31:0] out
);
wire [31:0] and_out, or_out, xor_out, nor_out;

and32 a1(a, b, and_out);
or32 a2(a, b, or_out);
xor32 a3(a, b, xor_out);
nor32 a4(a, b, nor_out);

mux32_4_2 mux(and_out, or_out, xor_out, nor_out, sel, out);

endmodule