use crate::commands::cmd::add_totals::AddTotalsCommand;
use crate::commands::cmd::bin::BinCommand;
use crate::commands::cmd::collect::CollectCommand;
use crate::commands::cmd::convert::ConvertCommand;
use crate::commands::cmd::data_model::DataModelCommand;
use crate::commands::cmd::dedup::DedupCommand;
use crate::commands::cmd::eval::EvalCommand;
use crate::commands::cmd::event_stats::EventStatsCommand;
use crate::commands::cmd::fields::FieldsCommand;
use crate::commands::cmd::fill_null::FillNullCommand;
use crate::commands::cmd::format::FormatCommand;
use crate::commands::cmd::head::HeadCommand;
use crate::commands::cmd::input_lookup::InputLookupCommand;
use crate::commands::cmd::join::JoinCommand;
use crate::commands::cmd::lookup::LookupCommand;
use crate::commands::cmd::make_results::MakeResultsCommand;
use crate::commands::cmd::map::MapCommand;
use crate::commands::cmd::multi_search::MultiSearchCommand;
use crate::commands::cmd::mv_combine::MvCombineCommand;
use crate::commands::cmd::mv_expand::MvExpandCommand;
use crate::commands::cmd::rare::RareCommand;
use crate::commands::cmd::regex::RegexCommand;
use crate::commands::cmd::rename::RenameCommand;
use crate::commands::cmd::return_::ReturnCommand;
use crate::commands::cmd::rex::RexCommand;
use crate::commands::cmd::s_path::SPathCommand;
use crate::commands::cmd::search::SearchCommand;
use crate::commands::cmd::sort::SortCommand;
use crate::commands::cmd::stats::StatsCommand;
use crate::commands::cmd::stream_stats::StreamStatsCommand;
use crate::commands::cmd::t_stats::TStatsCommand;
use crate::commands::cmd::table::TableCommand;
use crate::commands::cmd::tail::TailCommand;
use crate::commands::cmd::top::TopCommand;
use crate::commands::cmd::where_::WhereCommand;
use pyo3::pyclass;

#[allow(clippy::enum_variant_names)]
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum Command {
    AddTotalsCommand(AddTotalsCommand),
    BinCommand(BinCommand),
    CollectCommand(CollectCommand),
    ConvertCommand(ConvertCommand),
    DataModelCommand(DataModelCommand),
    DedupCommand(DedupCommand),
    EvalCommand(EvalCommand),
    EventStatsCommand(EventStatsCommand),
    FieldsCommand(FieldsCommand),
    FillNullCommand(FillNullCommand),
    FormatCommand(FormatCommand),
    HeadCommand(HeadCommand),
    InputLookupCommand(InputLookupCommand),
    JoinCommand(JoinCommand),
    LookupCommand(LookupCommand),
    MakeResultsCommand(MakeResultsCommand),
    MapCommand(MapCommand),
    MultiSearchCommand(MultiSearchCommand),
    MvCombineCommand(MvCombineCommand),
    MvExpandCommand(MvExpandCommand),
    RareCommand(RareCommand),
    RegexCommand(RegexCommand),
    RenameCommand(RenameCommand),
    ReturnCommand(ReturnCommand),
    RexCommand(RexCommand),
    SearchCommand(SearchCommand),
    SPathCommand(SPathCommand),
    SortCommand(SortCommand),
    StatsCommand(StatsCommand),
    StreamStatsCommand(StreamStatsCommand),
    TableCommand(TableCommand),
    TailCommand(TailCommand),
    TopCommand(TopCommand),
    TStatsCommand(TStatsCommand),
    WhereCommand(WhereCommand),
}
