import { ChangeEvent, FC, useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import { downloadAllDBData, getAllTables } from "../api/adminDashboardService";
import Swal from "sweetalert2";

export const AdminDashboard: FC = () => {
    const [tables, setTables] = useState<string[]>();
    const [selectedTable, setSelectedTable] = useState<string>();
    const [tableData, setTableData] = useState<any[]>([]);

    useEffect(() => {
        const getTables = async () => {
            try {
                const result = await getAllTables();
                setTables(result.data.tables);
            } catch (e) {
                console.error(e);
            }
        };
        getTables();
    }, []);

    const selectTable = (e: ChangeEvent<HTMLSelectElement>) => {
        setSelectedTable(e.target.value);
    };

    const downloadAllData = async () => {
        if (!selectedTable) return;
        try {
            const response = await downloadAllDBData(selectedTable);
            setTableData(response.data);
            downloadFile(response.data, `${selectedTable}.csv`);
        } catch (e) {
            console.error(e);
            Swal.fire({
                title: "Chyba",
                text: "Nepodařilo se stáhnout data",
                icon: "error",
                showConfirmButton: false,
            });
        }
    };

    const downloadFile = (data: any[], fileName: string) => {
        const csvContent = createCSVContent(data);
        const blob = new Blob([csvContent], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        a.click();
        URL.revokeObjectURL(url);
    }

    const createCSVContent = (data: any[]): string => {
        if (!data ||data.length === 0) return "";

        const keys = Object.keys(data[0]);
        const csvRows = [
            keys.join(","),
            ...data.map(row => keys.map(key => row[key]).join(","))
        ];

        return csvRows.join("\n");
    };

    return (
        <div className="container">
            <h1>Admin Dashboard</h1>
            <div className="row">
                <div className="col-sm-6">
                    <Form.Select aria-label="Vyberte, klteré data chcete stáhnout" onChange={selectTable}>
                        <option>Vyberte, které data chcete stáhnout</option>
                        {tables && tables.map((table) => (
                            <option value={table} key={table}>{table}</option>
                        ))}
                    </Form.Select>
                </div>
                <div className="col-sm-6">
                    {selectedTable && <Button variant="primary" onClick={downloadAllData}>Stáhnout všechna data z tabulky {selectedTable}</Button>}
                </div>
            </div>

            {tableData?.length > 0 && (
                <div className="mt-4">
                    <table className="table table-bordered">
                        <thead>
                        <tr>
                            {Object.keys(tableData[0]).map((key) => (
                                <th key={key}>{key}</th>
                            ))}
                        </tr>
                        </thead>
                        <tbody>
                        {tableData.map((row, index) => (
                            <tr key={index}>
                                {Object.keys(row).map((key) => (
                                    <td key={key}>{row[key]}</td>
                                ))}
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};
