module DFF(
    input D,
    input EN,
    input clk,
    output reg Q
);
reg out;

always @(posedge clk)
begin
  out = (EN) ? D : Q;
  Q = out;
end

endmodule