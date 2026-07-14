package org.project.javabackend.repo;

import org.project.javabackend.entity.AppointmentType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AppointmentTypeRepo extends JpaRepository<AppointmentType,Long> {
    Optional<AppointmentType> findByType(String type);
}
