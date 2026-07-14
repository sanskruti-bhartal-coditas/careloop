package org.project.javabackend.repo;

import org.project.javabackend.entity.OtpValidation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface OtpValidationRepo extends JpaRepository<OtpValidation,Long> {
}
