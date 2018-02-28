import execjs


ctx = execjs.compile("""
    function add(x, y) {
    return x + y;
    }
    """)
print(ctx.call("add", 1, 2))


test = execjs.compile("""
        function getBoundary(){
            var bdary = new BMap.Boundary();
            var name = document.getElementById("districtName").value;
            bdary.get(name, function(rs){       //获取行政区域
                map.clearOverlays();        //清除地图覆盖物
                var count = rs.boundaries.length; //行政区域的点有多少个
                for(var i = 0; i < count; i++){
                    var ply = new BMap.Polygon(rs.boundaries[i], {strokeWeight: 2, strokeColor: "#ff0000"}); //建立多边形覆盖物
                    map.addOverlay(ply);  //添加覆盖物
                    map.setViewport(ply.getPath());    //调整视野
                }
            });
        }
""")
