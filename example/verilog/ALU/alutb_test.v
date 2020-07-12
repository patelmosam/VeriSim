`include "example/verilog/ALU/alu32_test.v" 

module alutb_test;
reg [31:0] Input_x, Input_y;
reg [4:0] Input_control;
reg Input_cin;
wire monitor_overflow;
wire [31:0] monitor_out;

alu32_test uut(.monitor_overflow(monitor_overflow), .monitor_out(monitor_out), .Input_x(Input_x), .Input_y(Input_y), .Input_control(Input_control), .Input_cin(Input_cin));

initial begin
            
 // add your stimulas code here 

end

endmodule