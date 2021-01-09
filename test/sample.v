`include "components/gates/and.v" 
`include "components/gates/or.v" 

module test(monitor_m6, Input_m3, Input_m4, Input_m5);

input Input_m3, Input_m4, Input_m5;
output monitor_m6;


And m1(.out(m1_out), .in1(Input_m3), .in2(Input_m4));
Or m2(.c(monitor_m6), .a(m1_out), .b(Input_m5));

endmodule