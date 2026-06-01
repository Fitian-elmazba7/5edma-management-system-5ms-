import React from 'react';

interface DataTableColumn {
  key: string;
  label: string;
  render?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
  columns: DataTableColumn[];
  data: any[];
  onRowClick?: (row: any) => void;
  className?: string;
}

export const DataTable: React.FC<DataTableProps> = ({
  columns,
  data,
  onRowClick,
  className = '',
}) => {
  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-navy-deep/60 border-b-2 border-gold-primary">
            {columns.map((col) => (
              <th
                key={col.key}
                className="px-4 py-3 text-left text-xs font-bold uppercase text-gold-primary"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              onClick={() => onRowClick?.(row)}
              className="border-b border-navy-light/30 hover:bg-navy-light/40 transition-colors duration-200 cursor-pointer"
            >
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-cream text-sm">
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
