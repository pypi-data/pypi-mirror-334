from typing import Optional, Union, Dict, Sequence, List, Any

import wandb


class WandB:
    def __new__(
        cls,
        job_type: Optional[str] = None,
        dir: Optional[str] = None,
        config: Union[Dict, str, None] = None,
        project: Optional[str] = None,
        entity: Optional[str] = None,
        reinit: Optional[bool] = None,
        tags: Optional[Sequence] = None,
        group: Optional[str] = None,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        magic: Optional[Union[dict, str, bool]] = None,
        config_exclude_keys: Optional[List[str]] = None,
        config_include_keys: Optional[List[str]] = None,
        anonymous: Optional[str] = None,
        mode: Optional[str] = None,
        allow_val_change: Optional[bool] = None,
        resume: Optional[Union[bool, str]] = None,
        force: Optional[bool] = None,
        tensorboard: Optional[bool] = None,
        sync_tensorboard: Optional[bool] = None,
        monitor_gym: Optional[bool] = None,
        save_code: Optional[bool] = None,
        id: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):

        return wandb.init(
            job_type=job_type,
            dir=dir,
            config=config,
            project=project,
            entity=entity,
            reinit=reinit,
            tags=tags,
            group=group,
            name=name,
            notes=notes,
            magic=magic,
            config_exclude_keys=config_exclude_keys,
            config_include_keys=config_include_keys,
            anonymous=anonymous,
            mode=mode,
            allow_val_change=allow_val_change,
            resume=resume,
            force=force,
            tensorboard=tensorboard,
            sync_tensorboard=sync_tensorboard,
            monitor_gym=monitor_gym,
            save_code=save_code,
            id=id,
            settings=settings,
        )


if __name__ == "__main__":
    # Example usage:
    # wandb.init(project="my-project", entity="my-entity", name="my-run")
    run = WandB(
        project="my-project",
        entity="connectwithprakash",
        dir="./",
        name="my-run",
        mode="offiline",
    )
    run.log({"accuracy": 0.9})
    print("Run URL:", run.url)
    print(run.job_type)
    run.finish()
