`include "example/verilog/ALU/add_sub.v" 
`include "example/verilog/ALU/logic.v" 
`include "example/verilog/ALU/shifter32.v" 
`include "example/verilog/ALU/mux32_4_2.v" 

module alu32_test(monitor_overflow, monitor_out, Input_x, Input_y, Input_control, Input_cin);

input [31:0] Input_x, Input_y;
input [4:0] Input_control;
input Input_cin;
output monitor_overflow;
output [31:0] monitor_out;

wire [31:0] adder_sum, logic_out, shifter_out;

add_sub adder(.sum(adder_sum), .carry_out(monitor_overflow), .a({Input_y[31:16],Input_x[15:0]}), .b({Input_x[31:16],Input_y[15:0]}), .carry_in(Input_cin), .sel(Input_control[4]));
logic_unit logic(.out(logic_out), .a(Input_x), .b(Input_y), .sel(Input_control[3:2]));
shifter32 shifter(.out(shifter_out), .a(Input_x), .b(Input_y), .sel(Input_control[3:2]));
mux32_4_2 mux(.out(monitor_out), .in1(shifter_out), .in2(adder_sum), .in3(adder_sum), .in4(logic_out), .sel(Input_control[1:0]));

endmodule