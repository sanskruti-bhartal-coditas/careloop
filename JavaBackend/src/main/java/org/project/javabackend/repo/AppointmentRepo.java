package org.project.javabackend.repo;

import org.project.javabackend.entity.PatientAppointment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AppointmentRepo extends JpaRepository<PatientAppointment,Long> {
}
