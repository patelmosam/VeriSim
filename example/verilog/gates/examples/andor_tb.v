`include "example/verilog/gates/examples/andor.v" 

module andor_tb;
reg [1:0] Input_i1, Input_i2;
wire monitor_m1, monitor_m2;

andor uut(.monitor_m1(monitor_m1), .monitor_m2(monitor_m2), .Input_i1(Input_i1), .Input_i2(Input_i2));

initial begin
            
 // add your stimulas code here 

end

endmodule