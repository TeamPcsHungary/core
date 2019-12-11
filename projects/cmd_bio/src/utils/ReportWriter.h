#include <memory>
#include <map>
#include <string>
#include <vector>

#include <biogears/cdm/utils/Logger.h>

namespace biogears {

enum color
{
  Green = 0,
  Red = 1,
  Yellow = 2
};

class TableRow {
public:
  TableRow();
  TableRow(std::string field_name, std::string expected_value, double engine_value, std::string percent_error, std::string notes);
  ~TableRow();
  bool passed;
  std::string field_name; //field_name = value_name+unit_name
  std::string expected_value; //expected_value = reference_value+'@cite'+reference
  std::string percent_error; //
  std::string notes; //
  std::string table_name;
  double engine_value; //
  color result;
};

class ReferenceValue {
public:
  ReferenceValue();
  ~ReferenceValue();
  bool is_range;
  std::string value_name;
  std::string unit_name;
  std::string table_name;
  std::string reference;
  std::string notes;
  std::pair<double, double> reference_range;
  double reference_value;
  std::vector<double> reference_values;
  std::vector<std::pair<double, double>> reference_ranges;
};

class ReportWriter {
public:
  ReportWriter();
  ~ReportWriter();
  int to_table();
  void set_html();
  void set_md();
  void set_xml();
  void set_web();
  void gen_tables_single_sheet(const char* validation_file, const char* baseline_file, char table_type);
  void gen_tables_single_sheet(std::string validation_file, std::string baseline_file, char table_type);
  void gen_tables(char table_type);
  void ParseReferenceCSV(const char* filename);
  void ParseReferenceCSV(std::string filename);
  void ParseBaselineCSV(const char* filename);
  void ParseBaselineCSV(std::string filename);
  void CalculateAverages();
  void ExtractValues();
  void ExtractValuesList();
  void Validate();
  void PopulateTables();
  void clear(); // This does not reset the value of the pointers

private:
  void ParseCSV(std::string& filename, std::vector<std::vector<std::string>>& vec);
  void ParseXML(std::string& filename);
  std::map<std::string, std::vector<biogears::TableRow>> tables;
  std::map<std::string, biogears::TableRow> table_row_map;
  std::vector<biogears::ReferenceValue> reference_values;
  std::vector<std::vector<std::string>> validation_data;
  std::vector<std::vector<std::string>> biogears_results;
  std::string report;

  std::unique_ptr<biogears::Logger> logger;
  char* _body_begin;
  char* _table_begin;
  char* _table_row_begin;
  char* _table_row_begin_green;
  char* _table_row_begin_red;
  char* _table_row_begin_yellow;
  char* _table_second_line;
  char* _table_item_begin;
  char* _table_item_end;
  char* _table_row_end;
  char* _table_end;
  char* _body_end;
  char* _file_extension;
};

} // end namespace biogears