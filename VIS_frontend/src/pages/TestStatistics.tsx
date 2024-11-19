import {FC, useEffect, useLayoutEffect, useState} from "react";
import {useParams} from "react-router-dom";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {getStatisticsForTest} from "../api/statisticsService.ts";

export const TestStatistics:FC = () => {
    const {id} = useParams();
    const [data, setData] = useState([{
        category: "Jan",
        value1: 50,
    }]);

    const parseToAmchartData = (data: {student: string; success: number;}[]) => {
        return data.map((item: any) => {
            return {
                category: item.student,
                value1: item.success,
            };
        });
    }

    useEffect(() => {
        if (!id) return;
        const fetchData = async () => {
            try {
                const result = await getStatisticsForTest(id);
                setData(parseToAmchartData(result.data));
            } catch (error) {
                console.error(error);
            }
        }
        fetchData();
    }, [id]);

    useLayoutEffect(() => {
        let root = am5.Root.new("chartdiv");

        root.setThemes([
            am5themes_Animated.new(root)
        ]);

        let chart = root.container.children.push(
            am5xy.XYChart.new(root, {
                panY: false,
                layout: root.verticalLayout
            })
        );

        let yAxis = chart.yAxes.push(
            am5xy.ValueAxis.new(root, {
                renderer: am5xy.AxisRendererY.new(root, {})
            })
        );

        let xAxis = chart.xAxes.push(
            am5xy.CategoryAxis.new(root, {
                renderer: am5xy.AxisRendererX.new(root, {}),
                categoryField: "category"
            })
        );
        xAxis.data.setAll(data);

        let series1 = chart.series.push(
            am5xy.ColumnSeries.new(root, {
                name: "Úspěšnost",
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: "value1",
                categoryXField: "category"
            })
        );
        series1.data.setAll(data);
        let legend = chart.children.push(am5.Legend.new(root, {}));
        legend.data.setAll(chart.series.values);
        chart.set("cursor", am5xy.XYCursor.new(root, {}));

        return () => {
            root.dispose();
        };
    }, [data]);


    return (
        <div>
            <h1>Statistiky</h1>
            {data && data.map((score) => (
                <div key={score.category}>
                    <p>{score.category} vyplnil/a na <span style={{color: score.value1 === 100 ? "green" : "red"}}>{score.value1} %</span></p>
                </div>
            ))}
            <div id="chartdiv" style={{ width: "80%", height: "800px" }}></div>
        </div>
    )
}
