import { FC, useEffect, useLayoutEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getStatisticsForQuestion } from "../api/statisticsService.ts";
import * as am5 from "@amcharts/amcharts5";
import * as am5percent from "@amcharts/amcharts5/percent";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import am5themes_Dark from "@amcharts/amcharts5/themes/Dark";

export const QuestionStatistics: FC = () => {
    const { id } = useParams();
    const [rawData, setRawData] = useState<{ user: string; solution: string; is_correct: boolean }[]>([]);
    const [chartData, setChartData] = useState<{ category: string; value: number }[]>([]);

    const parseToPieChartData = (data: { user: string; solution: string; is_correct: boolean }[]) => {
        const groupedData: Record<string, number> = {};

        data.forEach((item) => {
            const key = item.is_correct ? "Správné odpovědi" : "Špatné odpovědi";
            groupedData[key] = (groupedData[key] || 0) + 1;
        });

        return Object.entries(groupedData).map(([category, value]) => ({
            category,
            value,
        }));
    };

    useEffect(() => {
        if (!id) return;

        const fetchData = async () => {
            try {
                const result = await getStatisticsForQuestion(id);
                setRawData(result.data);
                setChartData(parseToPieChartData(result.data));
            } catch (error) {
                console.error(error);
            }
        };

        fetchData();
    }, [id]);

    useLayoutEffect(() => {
        let root = am5.Root.new("chartdiv");

        // Set themes
        if (
            window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: dark)").matches
        ) {
            root.setThemes([am5themes_Animated.new(root), am5themes_Dark.new(root)]);
        } else {
            root.setThemes([am5themes_Animated.new(root)]);
        }

        // Create chart
        let chart = root.container.children.push(
            am5percent.PieChart.new(root, {
                layout: root.verticalLayout,
            })
        );

        // Create series
        let series = chart.series.push(
            am5percent.PieSeries.new(root, {
                valueField: "value",
                categoryField: "category",
            })
        );

        series.data.setAll(chartData);

        // Add legend
        chart.children.push(
            am5.Legend.new(root, {
                centerX: am5.percent(50),
                x: am5.percent(50),
                marginTop: 15,
                marginBottom: 15,
            })
        );

        // Animate chart appearance
        series.appear(1000, 100);

        return () => {
            root.dispose();
        };
    }, [chartData]);

    return (
        <div className="container mt-2">
            <h1>Statistika odpovědí</h1>
            {rawData.map((score, index) => (
                <div key={`${score.user}-${index}`}>
                    <p>
                        {score.user} napsal/a na{" "}
                        <span style={{ color: score.is_correct ? "green" : "red" }}>
              {score.solution}
            </span>
                    </p>
                </div>
            ))}
            <div id="chartdiv" style={{ width: "80%", height: "800px" }}></div>
        </div>
    );
};
