#include "vidur/execution_time_predictor/execution_time_predictor_pybind.h"

#include <pybind11/stl.h>
#include "vidur/execution_time_predictor/execution_time_predictor.h"

namespace vidur {
namespace execution_time_predictor {

namespace py = pybind11;

void InitExecutionTimePredictor(pybind11::module_& m)
{
    py::class_<ExecutionTimePredictor, std::shared_ptr<ExecutionTimePredictor>>(m, "ExecutionTimePredictor")
        .def(
            py::init<
                config::ExecutionTimePredictorConfig,
                config::ReplicaConfig,
                config::ModelConfig,
                std::vector<std::string>&,
                std::vector<std::vector<std::pair<int,int>>>&,
                std::vector<std::vector<double>>&>(),
            py::arg("config"),
            py::arg("replica_config"),
            py::arg("model_config"),
            py::arg("prediction_ops"),
            py::arg("prediction_keys"),
            py::arg("prediction_values"))
        .def(
            "get_execution_time_batch",
            &ExecutionTimePredictor::GetExecutionTimeBatch,
            py::arg("batch"),
            py::arg("pipeline_stage"))
        .def(
            "get_execution_time_kv_parallel_batch",
            &ExecutionTimePredictor::GetExecutionTimeKVParallelBatch,
            py::arg("kvp_batch"),
            py::arg("pipeline_stage"))
        .def("as_capsule", [](std::shared_ptr<ExecutionTimePredictor> self) {
        auto* sp_copy = new std::shared_ptr<ExecutionTimePredictor>(self);
        return py::capsule(
            sp_copy,
            "ExecutionTimePredictorPtr",
            [](PyObject *capsule) {
                auto* raw = static_cast<std::shared_ptr<ExecutionTimePredictor>*>(
                    PyCapsule_GetPointer(capsule, "ExecutionTimePredictorPtr")
                );
                delete raw;  // Freed when capsule is GC'd
            }
        );
    });
}

} // namespace execution_time_predictor
} // namespace vidur
