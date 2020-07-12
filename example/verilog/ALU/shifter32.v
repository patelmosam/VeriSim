`include "shift_left32.v"
//`include "shift_right32.v"
//`include "mux32_4_2.v"

module shifter32(
    input [31:0] a,
    input [31:0] b,
    input [1:0] sel,
    output [31:0] out
);
wire [31:0] left_out, right_out;

shift_left32 s1(.a(a), .b(b), .out(left_out));
shift_right32 s2(.a(a), .b(b), .out(right_out));

mux32_4_2 mux_1(.in1(a), .in2(left_out), .in3(right_out), .in4(a), .sel(sel), .out(out));

endmodule