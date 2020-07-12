`include "example/verilog/gates/or.v" 
`include "example/verilog/gates/and.v" 

module andor(monitor_m1, monitor_m2, Input_i1, Input_i2);

input [1:0] Input_i1, Input_i2;
output monitor_m1, monitor_m2;

wire [1:0] a1_out, a2_out;

Or o1(.c(monitor_m1), .a(a1_out[0]), .b(a2_out[0]));
Or o2(.c(monitor_m2), .a(a1_out[1]), .b(a2_out[1]));
and_2_1 a1(.out(a1_out), .in1(Input_i1), .in2(Input_i2));
and_2_1 a2(.out(a2_out), .in1(Input_i1), .in2(Input_i2));

endmodule