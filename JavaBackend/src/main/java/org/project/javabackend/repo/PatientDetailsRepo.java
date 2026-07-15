package org.project.javabackend.repo;

import org.project.javabackend.entity.PatientDetails;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PatientDetailsRepo extends JpaRepository<PatientDetails,Long> {
    PatientDetails findByUser_Id(Long userId);
}
