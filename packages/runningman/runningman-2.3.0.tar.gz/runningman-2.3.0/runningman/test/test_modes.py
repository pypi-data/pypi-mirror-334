# This code is part of runningman.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
from qiskit import *
from runningman.test import BACKEND, PROVIDER


def test_run_modes():
    """Test mode gets used by job"""
    qc = QuantumCircuit(5)
    qc.h(2)
    qc.cx(2, 1)
    qc.cx(1, 0)
    qc.cx(2, 3)
    qc.cx(3, 4)
    qc.measure_all()

    trans_qc = transpile(qc, BACKEND)
    mode = BACKEND.set_mode("batch")
    job = BACKEND.run(trans_qc, shots=135)
    BACKEND.close_mode()

    assert job.session_id == mode.session_id
    assert job.session_id == BACKEND.get_mode().session_id

    provider = PROVIDER
    job2 = provider.job(job.job_id())
    assert job2.session_id == mode.session_id
    BACKEND.clear_mode()


def test_mode_job_storage():
    """Validate that jobs in a mode are retrieved in the correct order"""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    trans_qc = transpile(qc, BACKEND)

    BACKEND.clear_mode()
    mode = BACKEND.set_mode("batch")
    jobs = []
    for _ in range(5):
        jobs.append(BACKEND.run(trans_qc, shots=2))

    for idx, job in enumerate(jobs):
        assert job.job_id == mode[idx].job_id


def test_mode_job_retrieval():
    """Validate that jobs in a mode are retrieved in the correct order"""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    trans_qc = transpile(qc, BACKEND)

    BACKEND.clear_mode()
    mode = BACKEND.set_mode("batch")
    for _ in range(5):
        BACKEND.run(trans_qc, shots=2)
    mode2 = PROVIDER.mode_from_id(mode.mode_id)
    for idx, job in enumerate(mode):
        assert job.job_id == mode2[idx].job_id
