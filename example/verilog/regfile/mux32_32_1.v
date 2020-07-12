module mux32_32_1(
    input [1023:0] data,
    input [4:0] sel,
    output reg [31:0] out
);

always @(sel)
begin
  case(sel)
    5'd0 : out = data[31:0];
    5'd1 : out = data[63:32];
    5'd2 : out = data[95:64];
    5'd3 : out = data[127:96];
    5'd4 : out = data[159:128];
    5'd5 : out = data[191:160];
    5'd6 : out = data[223:192];
    5'd7 : out = data[255:224];
    5'd8 : out = data[287:256];
    5'd9 : out = data[319:288];
    5'd10 : out = data[352:320];
    5'd11 : out = data[384:353];
    5'd12 : out = data[415:385];
    5'd13 : out = data[447:416];
    5'd14 : out = data[479:448];
    5'd15 : out = data[511:480];
    5'd16 : out = data[543:512];
    5'd17 : out = data[575:544];
    5'd18 : out = data[607:576];
    5'd19 : out = data[639:608];
    5'd20 : out = data[671:640];
    5'd21 : out = data[703:672];
    5'd22 : out = data[735:704];
    5'd23 : out = data[767:736];
    5'd24 : out = data[799:768];
    5'd25 : out = data[831:800];
    5'd26 : out = data[863:832];
    5'd27 : out = data[895:864];
    5'd28 : out = data[927:896];
    5'd29 : out = data[959:928];
    5'd30 : out = data[991:960];
    5'd31 : out = data[1023:992];

  endcase
end

endmodule