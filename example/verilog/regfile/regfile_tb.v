`include "example/verilog/regfile/regfile.v" 

module regfile_tb;
reg Input_clk, Input_WE;
reg [4:0] Input_RA1, Input_RA2, Input_WA;
reg [31:0] Input_WD;
wire [31:0] monitor_read1, monitor_read2;

regfile uut(.monitor_read1(monitor_read1), .monitor_read2(monitor_read2), .Input_clk(Input_clk), .Input_WE(Input_WE), .Input_RA1(Input_RA1), .Input_RA2(Input_RA2), .Input_WA(Input_WA), .Input_WD(Input_WD));

initial begin
            
 // add your stimulas code here 

end

endmodule