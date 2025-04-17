Coordinate Systems and Transformations Specification
====================================================

Table of Contents
-----------------

-  `Geometry <#geometry>`__

   -  `Basic concepts <#basic-concepts>`__
   -  `Basic Notation <#basic-notation>`__

      -  `Points and Vectors <#points-and-vectors>`__
      -  `Image/Volume Grids and
         Functions <#imagevolume-grids-and-functions>`__
      -  `Matrices <#matrices>`__

   -  `Right-handed Coordinate
      System <#right-handed-coordinate-system>`__
   -  `Transformation Matrices <#transformation-matrices>`__

      -  `3D Rotation Matrices <#3d-rotation-matrices>`__
      -  `3D Scaling Matrices <#3d-scaling-matrices>`__
      -  `3D Reflection Matrices <#3d-reflection-matrices>`__

   -  `3D Homogeneous Coordinates <#3d-homogeneous-coordinates>`__
   -  `Scalar Indices <#scalar-indices>`__

-  `Image/Volume Grids, Image/Volume Functions and their Coordinate
   Spaces <#imagevolume-grids-imagevolume-functions-and-their-coordinate-spaces>`__

   -  `2D Images <#2d-images>`__

      -  `Discrete Image Arrays to Continuous Image
         Functions <#discrete-image-arrays-to-continuous-image-functions>`__
      -  `Named 2D Image Arrays and
         Functions <#named-2d-image-arrays-and-functions>`__

   -  `3D Images <#3d-images>`__

      -  `Discrete Image Arrays to Continuous Image
         Functions <#discrete-image-arrays-to-continuous-image-functions-1>`__
      -  `Named 3D Image Arrays and
         Functions <#named-3d-image-arrays-and-functions>`__

-  `Coordinate Transformations <#coordinate-transformations>`__

   -  `Named 2D Transformations <#named-2d-transformations>`__
   -  `Named 3D Transformations <#named-3d-transformations>`__

-  `Tomographic Alignment <#tomographic-alignment>`__

-  `Subtomogram Alignment <#subtomogram-alignment>`__

-  `Annotations <#annotations>`__

   -  `Segmentation Annotations <#segmentation-annotations>`__
   -  `Set of Points Annotations <#set-of-points-annotations>`__

Geometry
--------

Basic concepts
~~~~~~~~~~~~~~

-  **Logical Space**: Continuous space in physical units of Angstroms
   (Å).
-  **Discrete Space**: Discrete array space with integer coordinates.

We explicitly define the discrete space to remove any ambiguity about
the location of the origin and the direction of the axes of the discrete
image, which has caused errors in the past.

Basic Notation
~~~~~~~~~~~~~~

Points and Vectors
^^^^^^^^^^^^^^^^^^

-  Discrete 2D coordinates are denoted as
   :math:`\mathbf{s^*} = (s^*_x, s^*_y)^T` where
   :math:`s^*_x, s^*_y \in \mathbb{Z}`
-  Discrete 3D coordinates are denoted as
   :math:`\mathbf{r^*} = (r^*_x, r^*_y, r^*_z)^T` where
   :math:`r^*_x, r^*_y, r^*_z \in \mathbb{Z}`
-  2D vectors are denoted as (lower case, bold face)
   :math:`\mathbf{s} = (s_x, s_y)^T` where
   :math:`s_x, s_y \in \mathbb{R}`
-  3D vectors are denoted as (lower case, bold face)
   :math:`\mathbf{r} = (r_x, r_y, r_z)^T` where
   :math:`r_x, r_y, r_z \in \mathbb{R}`

Image/Volume Grids and Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Discrete 2D image arrays are denoted as (capital, plain)

   .. math:: G^*[\mathbf{s}^*]: \mathbb{Z}^2 \rightarrow \mathbb{R}

   where :math:`\mathbf{N}_G = (n_x, n_y)` is the size of the image in
   pixels. :math:`n_x` is the **width** and :math:`n_y` is the
   **height** of the image.

-  Continuous 2D image functions are denoted as (capital, plain)

   .. math:: G(\mathbf{s}): \mathbb{R}^2 \rightarrow \mathbb{R}

-  Discrete 3D volume arrays are denoted as (capital, plain)

   .. math:: V^*[\mathbf{r}^*]: \mathbb{Z}^3 \rightarrow \mathbb{R}

   where :math:`\mathbf{N}_V = (n_x, n_y, n_z)` is the size of the
   volume in pixels. :math:`n_x` is the **width**, :math:`n_y` is the
   **height** and :math:`n_z` is the **depth** of the volume.

-  Continuous 3D volume functions are denoted as (capital, plain)

   .. math:: V(\mathbf{r}): \mathbb{R}^3 \rightarrow \mathbb{R}

Matrices
^^^^^^^^

-  Transformation matrices are denoted as (capital, bold face)
   :math:`\mathbf{M}`
-  Homogeneous transformation matrices are denoted as (capital, bold
   face with tilde) :math:`\tilde{\mathbf{M}}`

Right-handed Coordinate System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The standard coordinate system for cryoET is a right-handed Cartesian
coordinate system. The defining characteristic of a right-handed
coordinate system is the following set of relationships between the
vectors that constitute the coordinate system:

.. math:: \mathbf{x} \times \mathbf{y} = \mathbf{z}

.. math:: \mathbf{y} \times \mathbf{z} = \mathbf{x}

.. math:: \mathbf{z} \times \mathbf{x} = \mathbf{y}

Where :math:`\times` denotes the cross product and
:math:`\mathbf{x}, \mathbf{y}, \mathbf{z}` are the unit basis vectors.

The right-handed system is defined such that: - Electrons travel from
negative :math:`z` to positive :math:`z` (aligned with microscope
column) - :math:`y` points towards the microscopist - :math:`x` points
to the microscopist’s right

All points, vectors and transformations are defined with respect to the
right-handed coordinate system.

Transformation Matrices
~~~~~~~~~~~~~~~~~~~~~~~

Transformation matrices are used to represent geometrical
transformations between coordinate spaces. For a transformation from
space A to space B:

.. math:: \mathbf{s}_B = \mathbf{M}_{A \rightarrow B} \mathbf{s}_A

Where: - :math:`\mathbf{s}_A` is the coordinate in space A -
:math:`\mathbf{s}_B` is the coordinate in space B -
:math:`\mathbf{M}_{A \rightarrow B}` is the transformation matrix from
space A to space B

3D Rotation Matrices
^^^^^^^^^^^^^^^^^^^^

-  Right-handed 3D rotation about the x-axis by angle :math:`\alpha`:

   .. math::


      R_x(\alpha) = \begin{pmatrix}
      1 & 0 & 0 \\
      0 & \cos\alpha & \sin\alpha \\
      0 & -\sin\alpha & \cos\alpha
      \end{pmatrix}

-  Right-handed 3D rotation about the y-axis by angle :math:`\alpha`:

   .. math::


      R_y(\alpha) = \begin{pmatrix}
      \cos\alpha & 0 & -\sin\alpha \\
      0 & 1 & 0 \\
      \sin\alpha & 0 & \cos\alpha
      \end{pmatrix}

-  Right-handed 3D rotation about the z-axis by angle :math:`\alpha`:

   .. math::


      R_z(\alpha) = \begin{pmatrix}
      \cos\alpha & \sin\alpha & 0 \\
      -\sin\alpha & \cos\alpha & 0 \\
      0 & 0 & 1
      \end{pmatrix}

3D Scaling Matrices
^^^^^^^^^^^^^^^^^^^

-  3D scaling matrix with scaling factors :math:`s_x, s_y, s_z`:

.. math::


   S(s_x, s_y, s_z) = \begin{pmatrix}
   s_x & 0 & 0 \\
   0 & s_y & 0 \\
   0 & 0 & s_z
   \end{pmatrix}

3D Reflection Matrices
^^^^^^^^^^^^^^^^^^^^^^

-  3D reflection about the x-y plane:

.. math::


   F_{xy} = \begin{pmatrix}
   1 & 0 & 0 \\
   0 & 1 & 0 \\
   0 & 0 & -1
   \end{pmatrix}

-  3D reflection about the y-z plane:

.. math::


   F_{yz} = \begin{pmatrix}
   -1 & 0 & 0 \\
   0 & 1 & 0 \\
   0 & 0 & 1
   \end{pmatrix}

-  3D reflection about the x-z plane:

.. math::


   F_{xz} = \begin{pmatrix}
   1 & 0 & 0 \\
   0 & -1 & 0 \\
   0 & 0 & 1
   \end{pmatrix}

3D Homogeneous Coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~

Matrix operations on homogeneous coordinates are employed to represent
geometrical transformations:

.. math:: \tilde{r}_{F} = \tilde{\mathbf{M}}_F\tilde{r}

Where: - :math:`\tilde{r} \in \mathbb{R}^3 \times \{1\}` denotes the
homogeneous coordinate of the point undergoing transformation -
:math:`\tilde{r}_F = (x, y, z, 1) \in \mathbb{R}^3 \times \{1\}`
represents its transformed counterpart in homogeneous coordinates -
:math:`\tilde{\mathbf{F}}` is a 4×4 invertible matrix of real numbers,
structured as:

.. math::

   \tilde{\mathbf{M}}_F = \begin{pmatrix} 
   r_{11} & r_{12} & r_{13} & t_x \\
   r_{21} & r_{22} & r_{23} & t_y \\
   r_{31} & r_{32} & r_{33} & t_z \\
   0 & 0 & 0 & 1
   \end{pmatrix} = \begin{pmatrix}
   \mathbf{R} & \mathbf{t} \\
   0^T & 1
   \end{pmatrix}

Where: - :math:`\mathbf{R}` is a 3×3 rotation matrix -
:math:`\mathbf{t} = (t_x, t_y, t_z)^T` is a translation vector

Scalar Indeces
~~~~~~~~~~~~~~

-  :math:`i \in \mathbb{Z}` - The tilt index
-  :math:`j \in \mathbb{Z}` - The frame index
-  :math:`n \in \mathbb{Z}` - The sub-tomogram or sub-tiltstack index

Image/Volume Grids, Image/Volume Functions and their Coordinate Spaces
----------------------------------------------------------------------

Image Functions in cryoET processing are defined in terms of their
discrete and continuous representations.

2D Images
~~~~~~~~~

Discrete Image Arrays to Continuous Image Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a 2D image C:

.. math:: C^*[\mathbf{s}^*_C] = C(\mathbf{M}_C \mathbf{s}^*_C) = C(\mathbf{s}_C)

Where: - :math:`s^*_C` is the discrete coordinate in the image space -
:math:`s_C` is the continuous coordinate in the image space -
:math:`C^*[\cdot]` is the discrete image array in discrete space -
:math:`C(\cdot)` is the continuous image function in logical space -
:math:`\mathbf{M}_C` is the transformation matrix from the discrete
space to the continuous image or volume space

Matrix :math:`\mathbf{M}_C` encodes the translation and scaling
operations that map the discrete image space to the continuous image
space in that order, and is thus composed of a translation matrix
:math:`\mathbf{T}_C(t_x, t_y)` and a scaling matrix
:math:`\mathbf{S}_C(s_x, s_y)`:

.. math:: \mathbf{M}_C = \mathbf{S}_C \mathbf{T}_C

By default, the origin of the discrete image space is assumed to be at
:math:`\lfloor \frac{\mathbf{N}_C}{2} \rfloor`:

.. math::


   \mathbf{M}_C = \begin{pmatrix}
   s_x & 0 & s_x \lfloor 0.5n_x \rfloor \\
   0 & s_y & s_y \lfloor 0.5n_y \rfloor \\
   0 & 0 & 1
   \end{pmatrix}

Named 2D Image Arrays and Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------+-----------------+---------------------------------+-------+
| Entity  | Array/Function  | Discrete/Continuous Coords      | D->C  |
|         |                 |                                 | Tran  |
|         |                 |                                 | sform |
+=========+=================+=================================+=======+
| Cali    | :math:`C^*[\c   | :math:`\                        | :     |
| bration | dot], C(\cdot)` | mathbf{s}^*_C \in \mathbb{Z}^2, | math: |
| Images  |                 |  \mathbf{s}_C \in \mathbb{R}^2` | `M_g` |
+---------+-----------------+---------------------------------+-------+
| Movie   | :m              | :math:`\                        | :     |
| Frame   | ath:`M^*_j[\cdo | mathbf{s}^*_M \in \mathbb{Z}^2, | math: |
|         | t], M_j(\cdot)` |  \mathbf{s}_M \in \mathbb{R}^2` | `M_M` |
+---------+-----------------+---------------------------------+-------+
| Pro     | :m              | :math:`\                        | :     |
| jection | ath:`P^*_i[\cdo | mathbf{s}^*_P \in \mathbb{Z}^2, | math: |
|         | t], P_i(\cdot)` |  \mathbf{s}_P \in \mathbb{R}^2` | `M_P` |
+---------+-----------------+---------------------------------+-------+
| Sub-Pro | :math:`S^*      | :math:`\                        | :     |
| jection | _{i,n}[\cdot],  | mathbf{s}^*_S \in \mathbb{Z}^2, | math: |
|         | S_{i,n}(\cdot)` |  \mathbf{s}_S \in \mathbb{R}^2` | `M_S` |
+---------+-----------------+---------------------------------+-------+

.. _d-images-1:

3D Images
~~~~~~~~~

.. _discrete-image-arrays-to-continuous-image-functions-1:

Discrete Image Arrays to Continuous Image Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a 3D volume V:

.. math:: V^*[\mathbf{r}^*_V] = V(\mathbf{M}_V \mathbf{r}^*_V) = V(\mathbf{r}_V)

Where: - :math:`\mathbf{r}^*_V` is the discrete coordinate in the 3D
image space - :math:`\mathbf{r}_V` is the continuous coordinate in the
3D image space - :math:`V^*[\cdot]` is the discrete volume array in
discrete space - :math:`V(\cdot)` is the continuous volume function in
logical space - :math:`\mathbf{M}_V` is the transformation matrix from
the discrete space to the continuous image or volume space

Matrix :math:`\mathbf{M}_V` encodes the translation and scaling
operations that map the discrete volume space to the continuous volume
space in that order, and is thus composed of a translation matrix
:math:`\mathbf{T}_V(t_x, t_y, t_z)` and a scaling matrix
:math:`\mathbf{S}_V(s_x, s_y, s_z)`:

.. math:: \mathbf{M}_V = \mathbf{S}_V \mathbf{T}_V

By default, the origin of the discrete volume space is assumed to be at
:math:`\lfloor \frac{\mathbf{N}_V}{2} \rfloor`:

.. math::


   \mathbf{M}_V = \begin{pmatrix}
   s_x & 0 & 0 & s_x \lfloor 0.5 n_x \rfloor \\
   0 & s_y & 0 & s_y \lfloor 0.5 n_y \rfloor \\
   0 & 0 & s_z & s_z \lfloor 0.5 n_z \rfloor \\
   0 & 0 & 0 & 1
   \end{pmatrix}

#### Named 3D Image Arrays and Functions

+------------+-------------+----------------------------------+-------+
| Entity     | Sign        | Discrete/Continuous Coords       | D->C  |
|            | al/Function |                                  | Tran  |
|            |             |                                  | sform |
+============+=============+==================================+=======+
| Annotation | :math:      | :math:                           | :     |
|            | `A^*[\cdot] | `\mathbf{r}^*_A \in \mathbb{Z}^3 | math: |
|            | , A(\cdot)` | , \mathbf{r}_A \in \mathbb{R}^3` | `M_A` |
+------------+-------------+----------------------------------+-------+
| Tomogram   | :math:      | :math:                           | :     |
|            | `V^*[\cdot] | `\mathbf{r}^*_V \in \mathbb{Z}^3 | math: |
|            | , V(\cdot)` | , \mathbf{r}_V \in \mathbb{R}^3` | `M_V` |
+------------+-------------+----------------------------------+-------+
| S          | :math:`T^*  | :math:                           | :     |
| ubtomogram | _n[\cdot],  | `\mathbf{r}^*_T \in \mathbb{Z}^3 | math: |
|            | T_n(\cdot)` | , \mathbf{r}_T \in \mathbb{R}^3` | `M_T` |
+------------+-------------+----------------------------------+-------+
| Particle   | :math:      | :math:                           | :     |
| Reco       | `F^*[\cdot] | `\mathbf{r}^*_F \in \mathbb{Z}^3 | math: |
| nstruction | , F(\cdot)` | , \mathbf{r}_F \in \mathbb{R}^3` | `M_F` |
+------------+-------------+----------------------------------+-------+

Coordinate Transformations
--------------------------

Transformations between coordinate spaces are defined as:

:math:`\mathbf{s}_m = M_{c \rightarrow m} \mathbf{s}_c`

Where :math:`M_{c \rightarrow m}` represents the transformation matrix
from space c to space m.

Named 2D Transformations
~~~~~~~~~~~~~~~~~~~~~~~~

Useful transformations between 2D image spaces are defined as:

+--------------------+---------------------------------+---------------+
| Transformation     | Description                     | Matrix        |
+====================+=================================+===============+
| Calibration to     | Transform from calibration      | :             |
| Movie Frame        | image to movie frame            | math:`M_{C \r |
|                    |                                 | ightarrow M}` |
+--------------------+---------------------------------+---------------+
| Movie Frame to     | Transform from movie frame to   | :             |
| Projection         | projection                      | math:`M_{M \r |
|                    |                                 | ightarrow P}` |
+--------------------+---------------------------------+---------------+
| Sub-Projection to  | Transform from sub-projection   | :             |
| Projection         | to projection                   | math:`M_{S \r |
|                    |                                 | ightarrow P}` |
+--------------------+---------------------------------+---------------+

They MUST only be composed of the following transformations:

+------------------+-----------------------------------+---------------+
| Transformation   | Composition                       | Note          |
+==================+===================================+===============+
| Calibration to   | :math:`\mathbf{R}^{2D}({0,        | 90 deg        |
| Movie Frame      | 90, 180 270}), \mathbf{F}^{2D}_x` | rotations /   |
|                  |                                   | flip          |
+------------------+-----------------------------------+---------------+
| Movie Frame to   | :math:`\mathbf{T}`                | translation   |
| Projection       |                                   |               |
+------------------+-----------------------------------+---------------+
| Sub-Projection   | :math:`\mathbf{T}`                | translation   |
| to Projection    |                                   |               |
+------------------+-----------------------------------+---------------+

Named 3D Transformations
~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+-------------------------------+--------------+
| Transformation       | Description                   | Matrix       |
+======================+===============================+==============+
| Annotation to        | Transform from segmentation   | :ma          |
| Tomogram             | to tomogram                   | th:`M_{A \ri |
|                      |                               | ghtarrow V}` |
+----------------------+-------------------------------+--------------+
| Annotation Array to  | Transform from segmentation   | :math:`      |
| Tomogram Array       | array to tomogram array       | M_{A^* \righ |
|                      |                               | tarrow V^*}` |
+----------------------+-------------------------------+--------------+
| Subtomogram to       | Transform from subtomogram to | :ma          |
| Tomogram             | tomogram                      | th:`M_{T \ri |
|                      |                               | ghtarrow V}` |
+----------------------+-------------------------------+--------------+
| Particle             | Transform from particle       | :ma          |
| Reconstruction to    | reconstruction to tomogram    | th:`M_{F \ri |
| Tomogram             |                               | ghtarrow V}` |
+----------------------+-------------------------------+--------------+
| Particle             | Transform from particle       | :ma          |
| Reconstruction to    | reconstruction to subtomogram | th:`M_{F \ri |
| Subtomogram          |                               | ghtarrow T}` |
+----------------------+-------------------------------+--------------+

They MUST only be composed of the following transformations:

+-----------------------+--------------+-------------------------------+
| Transformation        | Composition  | Note                          |
+=======================+==============+===============================+
| Annotation to         | :math:       | scale, translation            |
| Tomogram              | `\mathbf{S}, |                               |
|                       |  \mathbf{T}` |                               |
+-----------------------+--------------+-------------------------------+
| Subtomogram to        | :math:       | rotations+translation         |
| Tomogram              | `\mathbf{R}, |                               |
|                       |  \mathbf{T}` |                               |
+-----------------------+--------------+-------------------------------+
| Particle              | :math:       | rotations+translation         |
| Reconstruction to     | `\mathbf{R}, |                               |
| Tomogram              |  \mathbf{T}` |                               |
+-----------------------+--------------+-------------------------------+
| Particle              | :math:       | rotations+translation         |
| Reconstruction to     | `\mathbf{R}, | (prior),                      |
| Subtomogram           |  \mathbf{T}` | rotations+translation         |
+-----------------------+--------------+-------------------------------+

Tomographic Alignment
---------------------

Tomographic alignment shall be defined by a single transformation matrix
:math:`\tilde{\mathbf{M}}_{V \rightarrow P, i}` per tilt that aligns
tomogram coordinates to the projection prior to projection.

.. math::


   \mathbf{s_P} = \begin{bmatrix}
   1 & 0 & 0 & 0 \\
   0 & 1 & 0 & 0 \\
   \end{bmatrix} \tilde{\mathbf{M}}_{V \rightarrow P, i} \tilde{\mathbf{\tilde{r_V}}}

An alignment matrix shall be reported for each tilt included in the
reconstruction of a particular tomogram.

Subtomogram Alignment
---------------------

Subtomogram alignment shall be defined by a single transformation matrix
:math:`\tilde{\mathbf{M}}_{F \rightarrow V, n}` per subtomogram or
sub-tiltstack that aligns particle reconstruction coordinates to its
predicted locatiion in the tomogram.

.. math::


   \tilde{\mathbf{r_V}} = \tilde{\mathbf{M}}_{F \rightarrow V, n} \tilde{\mathbf{r_F}}

An alignment matrix shall be reported for each subtomogram or
sub-tiltstack in a particular particle set.


Annotations
-----------

We define 3 types of basic annotations: - Segmentation: An image array
of numeric labels (see above) - Set of Points: A set of 2D or 3D points
with associated metadata - TriMesh: A set of 2D or 3D points and
connectivity table to form a triangular mesh

Segmentation Annotations
~~~~~~~~~~~~~~~~~~~~~~~~

Segmentation annotations are defined as a 2D or 3D image array of
numeric labels. Their spatial relationship to the tomogram is defined as
above. As a special case, it is allowed to define the segmentation array
in the same space as the tomogram, in which case the transformation
matrix :math:`M_{A \rightarrow V}` is the identity matrix.

Set of Points Annotations
~~~~~~~~~~~~~~~~~~~~~~~~~

A set of points is defined as a list of 2D or 3D coordinates with
associated metadata. The coordinates are defined in the same space as
the tomogram, or tomogram array, and the transformation matrix
:math:`M_{A \rightarrow V}` is the identity matrix.
