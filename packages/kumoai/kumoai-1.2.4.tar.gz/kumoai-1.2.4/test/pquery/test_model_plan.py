import pytest
from kumoapi.model_plan import ModelPlan, TaskType
from kumoapi.pquery import QueryType

from kumoai.client.pquery import filter_model_plan


def test_filter_model_plan() -> None:
    plan = ModelPlan(
        training_job=dict(
            num_experiments=1,
            metrics=['auc'],
            tune_metric='auc',
        ),
        neighbor_sampling=dict(
            max_target_neighbors_per_entity=[128],
            num_neighbors=[[16, 16]],
        ),
        optimization=dict(
            max_epochs=10,
            min_steps_per_epoch=30,
            max_steps_per_epoch=2000,
            max_val_steps=1000,
            max_test_steps=2000,
            loss=['binary_cross_entropy'],
            base_lr=[0.01, 0.001],
            weight_decay=[0.0],
            batch_size=[512, 1024],
            lr_scheduler=[
                dict(
                    name='constant_with_warmup',
                    interval='step',
                    kwargs=dict(warmup_ratio_or_steps=0.1),
                ),
                dict(
                    name='cosine_with_warmup_restarts',
                    interval='step',
                ),
            ],
            early_stopping=[dict(min_delta=0, patience=3)],
            majority_sampling_ratio=[None],
            weight_mode=['sample'],
        ),
        model_architecture=dict(
            channels=[64, 128],
            num_pre_message_passing_layers=[2],
            num_post_message_passing_layers=[2],
            aggregation=[['sum', 'mean', 'max']],
            activation=['relu', 'leaky_relu'],
            normalization=['layer_norm'],
            use_seq_id=[False],
            prediction_time_encodings=[False],
        ),
    )
    plan = filter_model_plan(
        plan=plan,
        task_type=TaskType.BINARY_CLASSIFICATION,
        query_type=QueryType.TEMPORAL,
    )

    assert plan.model_architecture.channels == [64, 128]

    with pytest.raises(AttributeError):
        plan.model_architecture.module

    assert repr(plan).startswith(('ModelPlan(\n'
                                  '  training_job=TrainingJobPlan(\n'
                                  '    num_experiments=1,'))

    assert 'disable_explain' not in repr(plan)  # Do not print hidden options.
    assert 'num_neighbors=[\n      [16, 16],' in repr(plan)
    assert 'EarlyStopping(min_delta=0.0, patience=3)' in repr(plan)
