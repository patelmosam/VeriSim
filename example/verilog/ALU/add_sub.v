`include "adder32.v"
`include "compliment2.v"

module add_sub(
    input [31:0] a,
    input [31:0] b,
    input carry_in,
    input sel,
    output [31:0] sum,
    output carry_out
);
wire [31:0] b1;
compliment2 comp(.in(b), .sel(sel), .out(b1));
adder32 add(.a(a), .b(b1), .carry_in(carry_in), .carry_out(carry_out), .sel(sel), .sum(sum));

endmodule